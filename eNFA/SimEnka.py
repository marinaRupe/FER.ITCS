import sys

def epsilon_closure(state):
    closure=list()
    closure.append(state)
    key=state+','+'$'
    
    for t in transitions:
        if t==key :
            state_list=transitions[t].split(',')
            for state in state_list:
                closure.append(state)           
    return closure

def next_states(state,symbol):
    states=list()
    key=state+','+symbol

    for t in transitions:
        if t==key :
            state_list=transitions[t].split(',')
            for state in state_list:
                if state != '#':
                    states.append(state)     
    return states

def epsilon_transitions(current_states):
    tryout=list()
    for state in current_states:
        tryout+=epsilon_closure(state)
    tryout=list(sorted(set(tryout)))

    while len(tryout)>len(current_states):
        current_states=tryout
        tryout=list()
        for state in current_states:
            tryout+=epsilon_closure(state)
        tryout=list(sorted(set(tryout)))
        
    return current_states


#INPUT: DEFINITION OF eNFA

input_lines = list()
for line in sys.stdin.readlines():
	line = line.strip() 
	if (len(line) > 0):
		input_lines.append(line)
	    

#DATA INITIALIZATION
first_line=input_lines[0].split('|')
input_array=list()
for input in first_line :
    input=input.split(',')
    input_array.append(input)

states=input_lines[1].split(',')
set_of_symbols=input_lines[2].split(',')
final_states=input_lines[3].split(',')
initial_state=input_lines[4]

transition_functions=list()
for i in range(5,len(input_lines)):
    transition_functions.append(input_lines[i])

transitions=dict()
for t in transition_functions:
    t_list=t.split('->', 2)
    key=t_list[0]
    value=t_list[1]
    transitions[key]=value


#AUTOMATA:
for input in input_array:

    current_states=sorted(set(epsilon_closure(initial_state)))
    current_states=epsilon_transitions(current_states)

    output_line=list()
    output_line.append(current_states)

    #INPUT ARRAY TESTING
    for symbol in input:
        
        if symbol in set_of_symbols:
            current=list()

            #next states
            for state in current_states:
                current+=next_states(state,symbol);

            #epsilon closures of next states
            current=list(sorted(set(current)))
            current_states=epsilon_transitions(current)
    
        else:
            current_states=list()

        output_line.append(current_states)

    #OUTPUT
    output=''
    for states in output_line:
        group_of_states=''

        if len(states)==0:
            group_of_states='# '
            
        else:
            for state in states:
                if state != '#':
                    group_of_states+=state+','
            
        output+=group_of_states[:-1]+'|'
        
    output=output[:-1]
    print output






