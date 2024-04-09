# Write an assembler @ command   
def a_command(s, address):
    s.append('@'+ str(address))
    
# Write an assembler C command
def c_command(s, dest, comp, jump=None):
    temp = ''
    if dest != None:
        temp += (dest+'=')
    temp+= comp
    if jump != None:
        temp+=(';'+jump)
    s.append(temp)
    
# Write an assembler L command
def l_command(s, label):
    s.append('('+label+')')
    
def load_sp(s):
    s.append('@SP')               # A=&SP
    s.append('A=M')             # A=SP

def dec_sp_pop(s):
    s.append('@SP')               # A=&SP
    s.append('M=M-1')
    s.append('A=M')             # A=SP
    s.append('D=M')
# SP operations
def inc_sp(s):
    a_command(s,'SP')               # A=&SP
    c_command(s,'M', 'M+1')         # SP=SP+1

#load value of segment to register
def load_seg (s,seg):
    s.append('@'+seg)
    s.append('D=M')

def load_index(s,index):
    num = int(index)
    comp = 'D=D+A'
    if(num < 0):
        num = - num
        index = str(num)
        comp = 'D=D-A'
    s.append('@'+str(index))
    s.append(comp)
    s.append('A=D')
    s.append('D=M')
    
def load_index_pop(s,index):
    num = int(index)
    comp = 'D=D+A'
    if(num < 0):
        num = - num
        index = str(num)
        comp = 'D=D-A'
    s.append('@'+str(index))
    s.append(comp)
    
# Global variable of file Name
# file_name = ''
# get name and save to global variable
def get_file_name(name):
    return name

    
def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    In the case of a variable, it is read from the specified memory segment using (base + index) 
    addressing.
    """
    s = [] 
        
    if segment == 'constant':
        # FIXME: complete the implementation
        a_command(s,index)
        c_command(s,'D','A')
        load_sp(s)
        c_command(s,'M','D')
        inc_sp(s)
        return s
    
    if segment in['local','this','that','argument']:
        if segment == 'local':
            load_seg(s,'LCL')
        elif segment == 'this':
            load_seg(s,'THIS')
        elif segment == 'that':
            load_seg(s,'THAT')
        else:
            load_seg(s,'ARG')
        load_index(s,index)
        load_sp(s)
        c_command(s,'M','D')
        inc_sp(s)
        return s
    
    if segment in ['pointer', 'temp']:
        if segment == 'temp':
            a_command(s,'5')
        elif segment == 'pointer':
            a_command(s,'3')
        c_command(s,'D','A')
        load_index(s,index)
        load_sp(s)
        c_command(s,'M','D')
        inc_sp(s)
        return s
    
    if segment == 'static':
        # Come back later
        temp_file = file_name +'.'+index
        load_seg(s,temp_file)
        load_sp(s)
        c_command(s,'M','D')
        inc_sp(s)
        return s
    
    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    
    return s

def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
    temp_resister = '13'        #temp resister number 13
    
    # FIXME: complete implmentation for local, argument, this, that, temp, pointer, and static segments.
    if segment in['local','this','that','argument']:
        if segment == 'local':
            load_seg(s,'LCL')
        elif segment == 'this':
            load_seg(s,'THIS')
        elif segment == 'that':
            load_seg(s,'THAT')
        else:
            load_seg(s,'ARG')
        load_index_pop(s,index)

        a_command(s,temp_resister)
        c_command(s,'M','D')
        dec_sp_pop(s)
        a_command(s,temp_resister)
        c_command(s,'A','M') 
        c_command(s,'M','D')
        return s
    
    if segment in ['pointer', 'temp']:
        if segment == 'temp':
            a_command(s,'5')
        elif segment == 'pointer':
            a_command(s,'3')
        a_command(s,'index')
        c_command(s,'D','D+A')
        dec_sp_pop(s)
        a_command(s,temp_resister)
        c_command(s,'A','M') 
        c_command(s,'M','D')
        return s
    
    if segment == 'static':
        # Come back later
        dec_sp_pop(s)
        temp_file = file_name +'.'+index
        a_command(s,temp_file)
        c_command(s,'M','D')
        inc_sp(s)
        return s
       
    return s

def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform the specified ALU operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
        # elif tokens[0] == 'add' or tokens[0] == 'sub' \
        #  or tokens[0] == 'mult' or tokens[0] == 'div' \
        #  or tokens[0] == 'or' or tokens[0] == 'and':
        
    # FIXME: complete implementation for + , - , | , and & operators
    if operation == 'add':
        dec_sp_pop(s)
        c_command(s,'A','A-1')
        c_command(s,'D','D+M')
        c_command(s,'M','D')
        return s
    if operation == 'sub':
        dec_sp_pop(s)
        c_command(s,'A','A-1')
        c_command(s,'D','M-D')
        c_command(s,'M','D')
        return s
    if operation == 'or':
        dec_sp_pop(s)
        c_command(s,'A','A-1')
        c_command(s,'M','D|M')
        return s
    if operation == 'and':
        dec_sp_pop(s)
        c_command(s,'A','A-1')
        c_command(s,'M','D&M')
        return s
    return s

def generate_unary_operation_code(operation):
    """Generate assembly code to perform the specified unary operation. 
    The operand is popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    
     # FIXME: complete implementation for bit-wise not (!) and negation (-) operatiors
    if operation == 'neg':
        a_command(s,'SP')
        c_command(s,'A','M-1') 
        c_command(s,'M','-M') 
        return s
    if operation == 'not':
        a_command(s,'SP')
        c_command(s,'A','M-1') 
        c_command(s,'M','!M') 
        return s
    return s
global file_name
file_name = get_file_name('abc.vm')
def push_registers_to_stack(s,label):
    s.append('@' + label)
    s.append('D=M')
    s.append('@SP')
    s.append('A=M')
    s.append('M=D')
    s.append('@SP')
    s.append('M=M+1')

def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []
    s.append('// goto [label]')
    s.append('@' + label)
    s.append('0;JMP')
    
    # FIXME
    
    return s
    
def generate_function_call_code(function, nargs, line_number):  
    """Generate preamble for function"""
    s = []
    temp_char = str(line_number)
    # FIXME: Push return address to stack
    s.append('// call function_name n_args')
    s.append('// Push return address to stack')
    s+=(generate_push_code('constant',temp_char))
    # FIXME: Push LCL, ARG, THIS, and THAT registers to stack
    s.append('// push LCL')
    push_registers_to_stack(s,'LCL')
    s.append('// push ARG')
    push_registers_to_stack(s,'ARG')
    s.append('// push THIS')
    push_registers_to_stack(s,'THIS')
    s.append('// push THAT')
    push_registers_to_stack(s,'THAT')
    # FIXME: Set ARG register to point to start of arguments in the current frame
    s.append('// ARG = SP-5-n')
    s.append('@SP')
    s.append('D=M')
    s.append('@' + nargs)
    s.append('D=D-A')
    s.append('@5')
    s.append('D=D-A')
    s.append('@ARG')
    s.append('M=D')
    # FIXME: Set LCL register to current SP
    s.append('// Set LCL register to current SP')
    s.append('@SP')
    s.append('D=M')
    s.append('@LCL')
    s.append('M=D')
    # FIXME: Generate goto code to jump to function 
    s.append('// Generate goto code')
    s += (generate_goto_code(function))
    # FIXME: Generate the pseudo-instruction/label corresponding to the return address
    s.append('//return-address')
    s.append('('+ temp_char + ')')
    
    return s
s=[]
# s += generate_push_code('constant', '3040')
# s += '/'
# s += generate_push_code('local', '-5')
# s += '/'
# s += generate_push_code('pointer', '0')
# s += '/'
# s += generate_push_code('argument', '1')
# s += '/'
# s += generate_push_code('static', '6')
# s += generate_pop_code('local','2')
s += generate_function_call_code('call','2',2)

# s += '/'
# temp_char = str(5)
# print(generate_push_code('constant',temp_char))

for i in range(100):
    print('xin loi')

