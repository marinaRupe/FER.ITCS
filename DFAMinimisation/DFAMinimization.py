import sys

def find_new_reachable_states(reachable_states, last_found_reachable_states):
    new_reachable_states = list()
    
    for reachable_state in last_found_reachable_states:
        for t in transitions:
            state_and_symbol = t.split(',')
            state = state_and_symbol[0]
            potential_state = transitions[t]
            
            if (reachable_state == state) and (potential_state not in reachable_states) :
                new_reachable_states.append(potential_state)
                
    new_reachable_states = list(sorted(set(new_reachable_states)))
    return new_reachable_states

def next_states(state):
    states=list()

    for s in set_of_symbols:
        state_and_symbol = state + ',' + s
        states.append(transitions[state_and_symbol])
    return states

def get_vector(list_of_next_states, groups):
    vector = ''
    for state in list_of_next_states:
        for group in groups:
            if state in group:
                vector += str(groups.index(group))      #find an index of the group that contains the next state
                break
    return vector
    

#INPUT: DFA DEFINITION
input_lines = list()
counter = 0
for line in sys.stdin.readlines():
    line = line.strip()
    counter+=1
    if (len(line) > 0 or counter == 3):     #third line can be empty if there are no final states
        input_lines.append(line)
        
#DATA INITIALIZATION
states = input_lines[0].split(',')
set_of_symbols = input_lines[1].split(',')
final_states = input_lines[2].split(',')
initial_state = input_lines[3]

transition_functions=list()
for i in range(4,len(input_lines)):
    transition_functions.append(input_lines[i])

transitions=dict()
for t in transition_functions:
    t_list=t.split('->', 2)
    key=t_list[0]
    value=t_list[1]
    transitions[key]=value


#DFA MINIMIZATION:
    
#FIND REACHABLE STATES
reachable_states = list()
reachable_states.append(initial_state)
last_found_reachable_states = list()
last_found_reachable_states.append(initial_state)
new_reachable_states = find_new_reachable_states(reachable_states, last_found_reachable_states)

while len(new_reachable_states) != 0:
    reachable_states += new_reachable_states
    reachable_states = list(sorted(set(reachable_states)))
    last_found_reachable_states = list()
    last_found_reachable_states += new_reachable_states
    new_reachable_states = find_new_reachable_states(reachable_states, last_found_reachable_states)

#REMOVE UNREACHABLE STATES
unreachable_states = list()
    
for state in states:
    if state not in reachable_states:
        unreachable_states.append(state)
states = reachable_states

new_final_states = list()
for state in final_states:
    if state not in unreachable_states:
        new_final_states.append(state)
final_states = new_final_states

new_transitions = dict()
for t in transitions:
    state_and_symbol = t.split(',')
    state = state_and_symbol[0]
    next_state = transitions[t]
    if (state not in unreachable_states) and (next_state not in unreachable_states):
        new_transitions[t] = next_state
transitions = new_transitions


#FIND EQUIVALENT STATES
#divide the acceptable and unacceptable states into two different groups
acceptable_states = list()
unacceptable_states = list()

list_of_next_states = dict()        #contains lists of next states for every state
for state in states:
    states_list = tuple(next_states(state))
    list_of_next_states[state] = states_list
    
    if state in final_states:
        acceptable_states.append(state)
    else:
        unacceptable_states.append(state)

groups = list()
new_groups = list()
if len(acceptable_states) != 0:
    new_groups.append(acceptable_states)
if len(unacceptable_states) != 0:
    new_groups.append(unacceptable_states)

while (len(new_groups) > len(groups)):
    groups = new_groups
    new_groups = list()
    
    for group in groups:
        list_of_vectors = dict()        #contains vectors (values) for every state (key) in a group
        unique_vectors = list()
        
        for state in group:
            vector = get_vector(list_of_next_states[state], groups)
            list_of_vectors[state] = vector
            unique_vectors.append(vector)
            
        unique_vectors = list(set(unique_vectors))
        number_of_different_vectors = len(unique_vectors)      #count how many different vectors are there

        #if all the vectors are not the same, divide the group
        if (number_of_different_vectors > 1):
            new_inside_groups = [[]] * number_of_different_vectors

            for state in list_of_vectors:
                vector = list_of_vectors[state]
                group_index = unique_vectors.index(vector)
                new_inside_groups[group_index] += [state] #add state to specified group
                new_inside_groups[group_index] = list(sorted(set(new_inside_groups[group_index])))

            new_groups += new_inside_groups

        else:
            new_groups.append(group)

                        
transitions_output = list()
for t in transitions:
    transition = t + '->' + transitions[t]
    transitions_output.append(transition)
transitions_output = list(sorted(set(transitions_output)))

#REMOVE EQUIVALENT STATES
for group in new_groups:
    for state in group:
        if state != group[0]:
            states.remove(state)

            if state in final_states:
                final_states.remove(state)
                
            if initial_state == state:
                initial_state = group[0]

            new_transitions_output = list()
            for t in transitions_output:
                t_list=t.split('->', 2)
                state_and_symbol = t_list[0].split(',', 2)
                previous_state = state_and_symbol[0]
                symbol = state_and_symbol[1]
                next_state = t_list[1]
                if (previous_state == state):
                    previous_state = group[0]
                    
                if (next_state == state):
                    next_state = group[0]
                    
                new_transitions_output.append(previous_state + ',' + symbol + '->' + next_state)
                
            transitions_output = new_transitions_output
        
#OUTPUT - MINIMIZED AUTOMATA DEFINITION
states_output = ''
for state in states:
    states_output += (state + ',')
states_output = states_output[:-1]

symbol_output = ''
for symbol in set_of_symbols:
    symbol_output += (symbol + ',')
symbol_output = symbol_output[:-1]

final_states_output = ''
for state in final_states:
    final_states_output += (state + ',')
final_states_output = final_states_output[:-1]

transitions_output = list(sorted(set(transitions_output)))

print states_output
print symbol_output
print final_states_output
print initial_state
for transition in transitions_output:
    print transition







