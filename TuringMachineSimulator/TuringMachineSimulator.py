import sys

#INPUT
input_lines = list()
for line in sys.stdin.readlines():
	line = line.strip()
	if (len(line) > 0 or line == '\n'):
		input_lines.append(line)

states = input_lines[0].split(',')
input_symbols = input_lines[1].split(',')
tape_symbols = input_lines[2].split(',')
empty_cell_symbol = input_lines[3]
tape = list(input_lines[4])
final_states = input_lines[5].split(',')
initial_state = input_lines[6]
initial_head_position = int(input_lines[7])

transitions = dict()
for i in range(8,len(input_lines)):
	t_list = input_lines[i].split('->', 2)
	key = t_list[0]
	value = t_list[1]
	transitions[key] = value

#TURING MACHINE SIMULATOR
current_state = initial_state
head_position = initial_head_position
while (True):
	tape_symbol = tape[head_position]
	key = current_state + ',' + tape_symbol

	if (transitions.get(key) is not None):
		value = transitions.get(key).split(',')
		tape[head_position] = value[1]
		head_shift = value[2]

		if (head_shift == 'L'):
			new_head_position = head_position - 1
		elif (head_shift == 'R'):
			new_head_position = head_position + 1

		if (new_head_position < 0 or new_head_position > 69): break
		else: head_position = new_head_position

		current_state = value[0]
	else: break

tape_string = ''.join(tape)
if (current_state in final_states):
	accepted = '1'
else:
	accepted = '0'

#OUTPUT
output = current_state + '|' + str(head_position) + '|' + tape_string + '|' + accepted
print output