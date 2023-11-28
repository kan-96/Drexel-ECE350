# -*- coding: utf-8 -*-
"""
Compiler back end for the Hack processor.
Translates from a stack-based language for the virtual machine to Hack assembly 

Author: Naga Kandasamy
Date created: September 1, 2020
Date modified: November 16, 2023

Student name(s): Khoa Nguyen    
Date modified: 11/20/2023
"""
import os
import sys


def generate_exit_code():
    """Generate some epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('(THATS_ALL_FOLKS)')
    s.append('@THATS_ALL_FOLKS')
    s.append('0;JMP')
    return s

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
        temp_file = file_name_global +'.'+index
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
        c_command(s,'D','A')
        a_command(s,index)
        c_command(s,'D','D+A')
        a_command(s,temp_resister)
        c_command(s,'M','D')
        dec_sp_pop(s)
        a_command(s,temp_resister)
        c_command(s,'A','M') 
        c_command(s,'M','D')
        return s
    
    if segment == 'static':
        # Come back later
        dec_sp_pop(s)
        temp_file = file_name_global +'.'+index
        a_command(s,temp_file)
        c_command(s,'M','D')
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


def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and the result of the operation 
    placed back in the stack.
    """
    s = []
    label_1 = ''
    label_2 = ''
    
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer
    s.append('A=M')
    s.append('D=M')             # D  = operand2
    s.append('@SP')
    s.append('M=M-1')           # Adjust stack pointer to get to operand #1
    s.append('A=M')
        
    if operation == 'lt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_LT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JLT')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')
        
   
    # FIXME: complete implementation for eq and gt operations
    if operation == 'eq':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_EQ_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JEQ')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')
        
    if operation == 'gt':
        s.append('D=M-D')       # D = operand1 - operand2
        label_1 = 'IF_GT_' + str(line_number)
        s.append('@' + label_1)
        s.append('D;JGT')       # if operand1 < operand2 goto IF_LT_*
        s.append('@SP')
        s.append('A=M')
        s.append('M=0')          # Push result on stack 
        s.append('@SP')
        s.append('M=M+1')
        label_2 = 'END_IF_ELSE_' + str(line_number)
        s.append('@' + label_2)
        s.append('0;JMP')
        s.append('(' + label_1 + ')')
        s.append('@SP')
        s.append('A=M')
        s.append('M=-1')        # Push result on stack
        s.append('@SP')
        s.append('M=M+1')
        s.append('(' + label_2 + ')')
        
    return s
  
def generate_set_code(register, value):
    """Generate assembly code for set"""
    s = []
    
    s.append('@' + value)
    s.append('D=A')
    
    if register == 'sp':
        s.append('@SP')
    
    if register == 'local':
        s.append('@LCL')
    
    if register == 'argument':
        s.append('@ARG')
        
    if register == 'this':
        s.append('@THIS')
        
    if register == 'that':
        s.append('@THAT')
        
    s.append('M=D')
    
    return s

# Global variable of file Name
file_name_global = ''
# get name and save to global variable
def get_file_name(name):
    return name

def translate(tokens, line_number):
    """Translate a VM command/statement into the corresponding Hack assembly commands/statements."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'mult' or tokens[0] == 'div' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
      
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
    
    elif tokens[0] == 'end':
        s = generate_exit_code()
        
    else:
        print('translate: Unknown operation')           # Unknown operation 
    
    return s

def run_vm_translator(file_name):
    """Main translator code. """
    assembly_code = []
    line_number = 1
    with open(file_name, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('\n')).split()
            
            # Ignore blank lines
            if not tokens:
                continue            
            
            if tokens[0] == '//':
                continue                                # Ignore comment       
            else:
                s = translate(tokens, line_number)
                line_number = line_number + 1
            
            if s:
                for i in s:
                    assembly_code.append(i)
            else:
                assembly_code = []
                return assembly_code
    
    return assembly_code

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python vm_translator.py file-name.vm")
        print("Example: Python vm_translator.py mult.vm")
    else:
        print("Translating VM file:", sys.argv[1])
        print()
        file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
        output_file = file_name_minus_extension + '.asm'
        file_name_global = sys.argv[1]
        assembly_code = run_vm_translator(sys.argv[1])
        if assembly_code:
            print('Assembly code generated successfully');
            print('Writing output to file:', output_file)
            # print(file_name_global)
            f = open(output_file, 'w')
            for s in assembly_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating assembly code')