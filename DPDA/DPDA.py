import sys

def check(stack, current_state, output, current_stack_symbol, input_symbol, failed):        
    
    if len(stack) != 0 :
        current_stack_symbol = stack[0]  #take symbol from the stack
        stack = stack[1:]
    else:
        current_stack_symbol = '$'
        
    key = current_state + ',' + input_symbol + ',' + current_stack_symbol
    key_empty = current_state + ',' + '$' + ',' + current_stack_symbol
    if key in transitions:
        next = transitions[key].split(',')
        current_state = next[0]
        stack_string = next[1]
                
        if stack_string != '$':
                stack = stack_string + stack  #insert at the beginning
                
        if len(stack) != 0:
                output+=current_state + '#' + stack + '|'
        else:
            output+=current_state + '#' + '$' + '|'
                
    elif key_empty in transitions:
        next = transitions[key_empty].split(',')
        current_state = next[0]
        stack_string = next[1]
            
        if stack_string != '$':
            stack = stack_string + stack  #insert at the beginning
                
        if len(stack) != 0:
            output+=current_state + '#' + stack + '|'
        else:
            output+=current_state + '#' + '$' + '|'
                
        new = check (stack, current_state, output, current_stack_symbol, input_symbol, failed)
        stack = new[0]
        current_state = new[1]
        output = new[2]
        failed = new[3]
        
    else:
        if failed == False:
            output+="fail|"
            failed = True
        
    return [stack, current_state, output, failed]
                    

#INPUT: DEFINITION OF DPA

input_lines = list()
for line in sys.stdin.readlines():
	line = line.strip() 
	if (len(line) > 0):
		input_lines.append(line)
	

#DATA INITIALIZATION
first_line = input_lines[0].split('|')
input_array = list()
for input in first_line :
    input = input.split(',')
    input_array.append(input)

states = input_lines[1].split(',')
set_of_symbols = input_lines[2].split(',')
stack_symbols = input_lines[3].split(',')
final_states = input_lines[4].split(',')
initial_state = input_lines[5]
initial_stack_symbol = input_lines[6]

transition_functions = list()
for i in range(7,len(input_lines)):
    transition_functions.append(input_lines[i])

transitions = dict()
for t in transition_functions:
    t_list = t.split('->', 2)
    key = t_list[0]
    value = t_list[1]
    transitions[key] = value
    

for input in input_array:
    current_state = initial_state
    next_stack_symbol = initial_stack_symbol
    stack = ''
    stack += initial_stack_symbol
    output = ''
    failed = False
    
    output+=current_state + '#' + stack + '|'
    
    for input_symbol in input:
        
        #print output
        #print input_symbol
        
        if len(stack) != 0 :
            current_stack_symbol = stack[0]      #take symbol from the stack
            stack = stack[1:]
        else:
            current_stack_symbol = '$'
        
        key = current_state + ',' + input_symbol + ',' + current_stack_symbol
        key_empty = current_state + ',' + '$' + ',' + current_stack_symbol
        if key in transitions:
            next = transitions[key].split(',')
            current_state = next[0]
            stack_string = next[1]
                
            if stack_string != '$':
                stack = stack_string + stack  #insert at the beginning
                
            if len(stack) != 0:
                output+=current_state + '#' + stack + '|'
            else:
                output+=current_state + '#' + '$' + '|'
                
        elif key_empty in transitions:
            next = transitions[key_empty].split(',')
            current_state = next[0]
            stack_string = next[1]
            
            if stack_string != '$':
                stack = stack_string + stack  #insert at the beginning
                
            if len(stack) != 0:
                output+=current_state + '#' + stack + '|'
            else:
                output+=current_state + '#' + '$' + '|'
                
                   
            new = check (stack, current_state, output, current_stack_symbol, input_symbol, failed)
            stack = new[0]
            current_state = new[1]
            output = new[2]
            failed = new[3]
        
        else:
            if failed == False:
                output+="fail|"
                failed = True
            break
        
        
    #OUTPUT    
    if (not failed and (current_state in final_states)):
        output+=str(1)
        
    elif (not failed):
        
        while (len(stack) != 0 and not (current_state in final_states)):
            failed = False
        
            current_stack_symbol = stack[0]  #take symbol from the stack
            stack = stack[1:]

            
            key = current_state + ',' + '$' + ',' + current_stack_symbol
            
            if key in transitions:
                next = transitions[key].split(',')
                current_state = next[0]
                stack_string = next[1]
                
                if stack_string != '$':
                    stack = stack_string + stack  #insert at the beginning
                
                if len(stack) != 0:
                    output+=current_state + '#' + stack + '|'
                else:
                    output+=current_state + '#' + '$' + '|'
                    
                if current_state in final_states:
                    break
                    
            else:
                failed = True
                break
            
        if (not failed and (current_state in final_states)): 
            output+=str(1)
            
        else:
            output+=str(0)
            
    else:
        output+=str(0)
                
    print output # ----> stanje1#stogZnak|stanje2#stogZnak|0 (ili 1)
