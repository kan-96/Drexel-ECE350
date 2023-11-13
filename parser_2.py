#remove all white space

def remove_whitespace(command):
    """Remove all whitespace from a given command."""
    return command.replace(" ", "")
valid_jmp_patterns =  {'null':'000',
                    'JGT':'001',
                    'JEQ':'010',
                    'JGE':'011',
                    'JLT':'100',
                    'JNE':'101',
                    'JLE':'110',
                    'JMP':'111'
                    }

def parse(command):
    """Implements finite automate to scan assembly statements and parse them.

    WHITE SPACE: Space characters are ignored. Empty lines are ignored.
    
    COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered 
    comment and is ignored.
    
    CONSTANTS: Must be non-negative and are written in decimal notation. 
    
    SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.), 
    dollar sign ($), and colon (:) that does not begin with a digit.
    
    LABEL: (SYMBOL)
    """

    
    # Data structure to hold the parsed fields for the command
    s = {}
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
    
    # Valid operands and operations for C-type instructions
    valid_operands = '01DMA'
    valid_operations = '+-&|'
    
    # Finite Automata
    state = 0
    current_token = ''
    
    command = remove_whitespace(command)
    for char in command:
        if state == 0:
            if char.isspace() or char == '\n':
                continue
            elif char == '@':
                s['instruction_type'] = 'A_INSTRUCTION'
                state = 1
            elif char == '/' :              #check for syntax error or comment
                state = 5
            else:                           #go to C-instruction section
                s['instruction_type'] = 'C_INSTRUCTION'
                state = 6
        elif state == 1:  # Check num or sym
            if char.isspace():
                continue
            elif char.isdigit():           # A-instruction
                current_token += char
                state = 3
            elif char.isalpha():           #
                current_token += char
                state = 2
            else:               #syntax error
                s['status'] = -1
                state = 5
        elif state == 2:  # SYMBOL
            if char.isalnum() or char in '_.$:':
                current_token += char
            else:
                s['value'] = current_token
                s['value_type'] = 'SYMBOL'
                current_token = ''
                if char.ispace():
                    state = 4
                elif char == '\n':
                    state =5
                else:        #syntax error
                    state = 5
                    s['status'] = -1

        elif state == 3:  # NUMERIC
            if char.isdigit():
                current_token += char
            else:
                s['value'] = current_token
                s['value_type'] = 'NUMERIC'
                current_token = ''
                if char.ispace():
                    state = 6
                elif char == '\n':
                    state = 5
                else:        #syntax error
                    state = 5
                    s['status'] = -1
        elif state == 4:  # LABEL, next state after symbol
            if char.ispace():
                state = 4
            elif char == '\n':          
                state =5
                s['value_type'] = ''
                s['dest'] = 'null'
                s['comp'] = ''
                s['jmp'] = 'null'
                s['status'] = 0

        elif state == 5:  # COMMENT/Status
            if char == '\n' or char == '.':
                state == 0
            elif char == '/':           # double-/ for comment section
                state = 9
        elif state == 6:  # Check for C-instruction
            if s['dest'] == '' and s['comp'] == '':
                if char in valid_operands:
                    current_token += char
                elif char == '=':
                    s['dest'] == current_token
                    current_token = ''
                elif char == ';':
                    s['comp'] == current_token
                    current_token = ''
            else:
                if s['jmp'] == '':
                    if char in valid_operations or char in valid_operands:
                        current_token += char
                    elif char == '\n':
                        s['comp'] == current_token
                        current_token = ''
                
        elif state == 7:            #check for comp condition
            if char in valid_operations or char in valid_operands:
                current_token += char
            elif char.isspace():
                continue
            elif char == "\n":                  # sucesss
                s['comp'] = current_token
                s['jmp'] = 'null'
                s['status'] = 0
                current_token =''
                state = 0
        elif state == 8:
            if char.isalpha():
                current_token += char
            elif char.isspace():
                continue
            elif char == '\n':
                state = 0
                if current_token in valid_jmp_patterns:
                    s['jmp'] = current_token
                    s['status'] = 0
                else:
                    s['status'] = -1
        elif state == 9:        #conmment state
            #ingnore the rest of the line
            break
    # Check if the tokens were formed correctly
    if state == 1 or state == 2 or state == 3 or state == 4 or state == 7:
        if current_token:
            if current_token.isdigit():
                s['value'] = current_token
                s['value_type'] = 'NUMERIC'
            elif current_token.isalnum() or current_token in '_.$:':
                s['value'] = current_token
                s['value_type'] = 'SYMBOL'
            elif current_token in valid_operands:
                s['dest'] = current_token
            else:
                s['comp'] = current_token
    
    return s

# Examples
command1 = "@100"
parsed1 = parse(command1)
print(parsed1)

command2 = "@sum"
parsed2 = parse(command2)
print(parsed2)

command3 = "D = D + M"
parsed3 = parse(command3)
print(parsed3)

instruction4 = "D;JGT"
parsed4 = parse(instruction4)
print(parsed4)
