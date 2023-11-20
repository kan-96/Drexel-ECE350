# -*- coding: utf-8 -*-
"""
Compiler back-end for the Hack processor.
Translates from a stack-based language for the virtual machine to the Hack assembly code.

Adds support for program flow and subroutines.

Author: Naga Kandasamy
Date created: September 1, 2020
Date modified: November 18, 2023


Student names(s):
Date modified: 
"""
import os
import sys

line_number = 1

def generate_exit_code():
    """Generate epilogue code that places the program, upon completion, into 
    an infinite loop. 
    """
    s = []
    s.append('(THATS_ALL_FOLKS)')
    s.append('@THATS_ALL_FOLKS')
    s.append('0;JMP')
    return s


def generate_push_code(segment, index):
    """Generate assembly code to push value into the stack.
    In the case of a variable, it is read from the specified memory segment using (base + index) 
    addressing.
    """
    s = [] 
    
    
    # FIXME
    
    return s
    
def generate_pop_code(segment, index):
    """Generate assembly code to pop value from the stack.
    The popped value is stored in the specified memory segment using (base + index) 
    addressing.
    """
    s = []
      
   
   # FIXME
    
    return s

def generate_arithmetic_or_logic_code(operation):
    """Generate assembly code to perform specified ALU operation. 
    The two operands are popped from the stack and result of operation 
    pushed back in the stack.
    """
    s = []

    # FIXME           
    
    return s

def generate_unary_operation_code(operation):
    """Generate assembly code to perform specified unary operation. 
    The operand is popped from the stack and result of operation 
    pushed back in the stack.
    """
    s = []
   
    # FIXME
    
    return s

def generate_relation_code(operation, line_number):
    """Generate assembly code to perform the specified relational operation. 
    The two operands are popped from the stack and result of the operation 
    pushed back in the stack.
    """
    s = []
    
    # FIXME
   
    return s
  

def generate_if_goto_code(label):
    """Generate code for the if-goto statement. 

    Behavior:
    
    1. Pop result of expression from stack.
    2. If result is non-zero, goto LABEL.
    
    """
    s = []
    
    # FIXME: complete implementation
    
    return s

def generate_goto_code(label):
    """Generate assembly code for goto."""
    s = []
    
    # FIXME
    
    return s

def generate_pseudo_instruction_code(label):   
    """Generate pseudo-instruction for label."""
    s = []
    
    s.append('(' + label + ')')
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

def generate_function_call_code(function, nargs, line_number):  
    """Generate preamble for function"""
    s = []
    
    # FIXME: Push return address to stack
    
    # FIXME: Push LCL, ARG, THIS, and THAT registers to stack
    
    # FIXME: Set ARG register to point to start of arguments in the current frame
    
    # FIXME: Set LCL register to current SP
    
    # FIXME: Generate goto code to jump to function 
    
    # FIXME: Generate the pseudo-instruction/label corresponding to the return address
    
    return s

def generate_function_body_code(f, nvars):
    """Generate code for function f.
    f: name of the function, which should be located in a separate file called f.vm
    n: number of local variables declared within the function.
    """
    s = []
    
    # FIXME: Generate the pseudo instruction -- the label
    
    # FIXME: Push nvars local variables into the stack, each intialized to zero
    
    return s


def generate_function_return_code():
    """Generate assembly code for function return"""
    s = []
    
    s.append('// Copy LCL to temp register R14 (FRAME)')
    # FIXME: Copy LCL to temp register R14 (FRAME)
    
    s.append('// Store return address in temp register R15 (RET)')
    # FIXME: Store return address in temp register R15 (RET)
    
    s.append('// Pop result from the working stack and move it to beginning of ARG segment')
    # FIXME: Pop result from the working stack and move it to beginning of ARG segment
    # FIXME: Adjust SP = ARG + 1
    
    
    # FIXME: Restore THAT = *(FRAME - 1)
    
    
    # FIXME: Restore THIS = *(FRAME - 2)
   
    
    # FIXME: Restore ARG = *(FRAME - 3)
    
    
    # FIXME: Restore LCL = *(FRAME - 4)
    
    
    # FIXME: Jump to return address stored in R15 back to the caller code
   
    return s

def translate_vm_commands(tokens, line_number):
    """Translate a VM command into corresponding Hack assembly commands."""
    s = []
    
    if tokens[0] == 'push':
        s = generate_push_code(tokens[1], tokens[2])    # Generate code to push into stack
        
    elif tokens[0] == 'pop':
        s = generate_pop_code(tokens[1], tokens[2])     # Generate code to pop from stack
        
    elif tokens[0] == 'add' or tokens[0] == 'sub' \
         or tokens[0] == 'or' or tokens[0] == 'and':
        s = generate_arithmetic_or_logic_code(tokens[0])  # Generate code for ALU operation
        
    elif tokens[0] == 'neg' or tokens[0] == 'not':
        s = generate_unary_operation_code(tokens[0])    # Generate code for unary operations
        
    elif tokens[0] == 'eq' or tokens[0] == 'lt' or tokens[0] == 'gt':
        s = generate_relation_code(tokens[0], line_number)
    
    elif tokens[0] == 'label':
        s = generate_pseudo_instruction_code(tokens[1])
    
    elif tokens[0] == 'if-goto':
        s = generate_if_goto_code(tokens[1]) 
        
    elif tokens[0] == 'goto':
        s = generate_goto_code(tokens[1])
    
    elif tokens[0] == 'end':
        s = generate_exit_code()
        
    elif tokens[0] == 'set':
        s = generate_set_code(tokens[1], tokens[2])
        
    elif tokens[0] == 'function':
        s = generate_function_body_code(tokens[1], int(tokens[2]))
        
    elif tokens[0] == 'call':
        s = generate_function_call_code(tokens[1], tokens[2], line_number)
        
    elif tokens[0] == 'return':
        s = generate_function_return_code()
        
    else:
        print('translate_vm_commands: Unknown operation')           # Unknown operation 
    
    return s
    
def translate_file(input_file):
    """Translate VM file to Hack assembly code"""
    global line_number
    assembly_code = []
    assembly_code.append('// ' + input_file)
    
    with open(input_file, 'r') as f:
        for command in f:        
            # print("Translating line:", line_number, command)
            tokens = (command.rstrip('\n')).split()
            
            if not tokens:
                continue                                        # Ignore blank lines  
            
            if tokens[0] == '//':
                continue                                        # Ignore comment       
            else:
                s = translate_vm_commands(tokens, line_number)
                line_number = line_number + 1        
            if s:
                
                for i in s:
                    assembly_code.append(i)
            else:
                return False
            
    # Write translated commands to .i file
    file_name_minus_extension, _ = os.path.splitext(input_file)
    output_file = file_name_minus_extension + '.i'
    out = open(output_file, 'w')
    for s in assembly_code:
        out.write('%s\n' %s)
    out.close()
    print('Assembly file generated: ', output_file)
        
    return True

def run_vm_to_asm_translator(path):
    """Main translator code"""
    files = os.listdir(path)
    
    cwd = os.getcwd()
    os.chdir(path)
    
    if 'sys.vm' in files:
        idx = files.index('sys.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing sys.vm file')
        return False
        
    if 'main.vm' in files:
        idx = files.index('main.vm')
        f = files.pop(idx)
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    else:
        print('Missing main.vm file')
        return False
    
    for f in files:
        print('Translating:', f)
        status = translate_file(f)
        if status == False:
            print('Error translating ', f)
            return False
    
    os.chdir(cwd)
    
    return True

def assemble_final_file(output_file, path):
    """Assemble final output file"""
    intermediate_files = []
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    with open(output_file, 'w') as outfile:    
        idx = intermediate_files.index('sys.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        idx = intermediate_files.index('main.i')
        f = intermediate_files.pop(idx)
        with open(f, 'r') as infile:
            for line in infile:
                outfile.write(line)
        
        for f in intermediate_files:
            with open(f, 'r') as infile:
                for line in infile:
                    outfile.write(line)

    os.chdir(cwd)
    return True
    
def clean_intermediate_files(path):
    """Removes intermediate .i files from supplied path"""
    intermediate_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.i'):
            intermediate_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in intermediate_files:
        os.remove(f)
    
    os.chdir(cwd)
        

def clean_old_files(path):
    """Removes old files from supplied path"""
    old_files = []
    
    files = os.listdir(path)
    for f in files:
        if f.endswith('.asm') or f.endswith('.i') or f.endswith('.hack'):
            old_files.append(f)
            
    cwd = os.getcwd()
    os.chdir(path)
    
    for f in old_files:
        os.remove(f)
    
    os.chdir(cwd)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: Python vm_translator_v2.py file-name.asm path-name")
        print("file-name.asm: assembly file to be generated by the translator")
        print("path-name: directory containing .vm source files")
        print("Example: Python vm_translator_v2.py mult-final.asm ./mult")
    else:
        output_file = sys.argv[1]
        path = sys.argv[2]
        clean_old_files(path)
        
        status = run_vm_to_asm_translator(path)
        if status == True:
            print('Intermediate assembly files were generated successfully');
            print('Generating final assembly file: ', output_file)
            assemble_final_file(output_file, path)
            # clean_intermediate_files(path)
        else:
            print('Error generating assembly code')