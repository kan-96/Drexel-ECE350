# -*- coding: utf-8 -*-
"""Assembler for the Hack processor.

Author: Naga Kandasamy
Date created: August 8, 2020
Date modified: November 9, 2023

Student name(s): Khoa Nguyen
Date modified: 11/10/2023
"""

import os
import sys
import re

"""The comp field is a c1 c2 c3 c4 c5 c6"""
valid_comp_patterns = {'0':'0101010', 
                       '1':'0111111',
                       '-1':'0111010',
                       'D':'0001100',
                       'A':'0110000',
                       '!D':'0001101',
                       '!A':'0110001',
                       '-D':'0001111',
                       '-A':'0110011',
                       'D+1':'0011111',
                       'A+1':'0110111',
                       'D-1':'0001110',
                       'A-1':'0110010',
                       'D+A':'0000010',
                       'D-A':'0010011',
                       'A-D':'0000111',
                       'D&A':'0000000',
                       'D|A':'0010101',
                       'M':'1110000',
                       '!M':'1110001',
                       '-M':'1110011',
                       'M+1':'1110111',
                       'M-1':'1110010',
                       'D+M':'1000010',
                       'M+D':'1000010',
                       'D-M':'1010011',
                       'M-D':'1000111',
                       'D&M':'1000000',
                       'D|M':'1010101'
                       }

"""The dest bits are d1 d2 d3"""
valid_dest_patterns = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'
                       }

"""The jump fields are j1 j2 j3"""
valid_jmp_patterns =  {'null':'000',
                       'JGT':'001',
                       'JEQ':'010',
                       'JGE':'011',
                       'JLT':'100',
                       'JNE':'101',
                       'JLE':'110',
                       'JMP':'111'
                       }

"""Symbol table populated with predefined symbols and RAM locations"""
valid_symbol_table = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0,
                'R1':1,
                'R2':2,
                'R3':3,
                'R4':4,
                'R5':5,
                'R6':6,
                'R7':7,
                'R8':8,
                'R9':9,
                'R10':10,
                'R11':11,
                'R12':12,
                'R13':13,
                'R14':14,
                'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }

def print_intermediate_representation(ir):
    """Print intermediate representation"""
    
    for i in ir:
        print()
        for key, value in i.items():
            print(key, ':', value)

        
def print_instruction_fields(s):
    """Print fields in instruction"""
    
    print()
    for key, value in s.items():
        print(key, ':', value)


def valid_tokens(s):
    """Return True if tokens belong to valid instruction-field patterns"""
    
    return True

def remove_whitespace(command):
    """Remove all whitespace from a given command."""
    return command.replace(" ", "")

def remove_last_char_if_newline(s):
    # Using rstrip to remove trailing whitespace, including newline characters
    return s.rstrip('\n')

def remove_comments(line):
    # Split the line based on '//', take the first part
    return line.split('//')[0]

def is_valid_symbol(symbol):
    # Define a regular expression pattern for a valid symbol
    pattern = re.compile(r'^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$')

    # Check if the symbol matches the pattern
    return bool(pattern.match(symbol))

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
    
    
    command = remove_whitespace(command)
    command = remove_last_char_if_newline(command)
    command = remove_comments(command)
    
    is_l_command = lambda i : i.find('(') != -1 and i.find(')') != -1    
    is_a_command = lambda i : i.find('@') != -1   
    is_c_command = lambda i : i.find("(") == -1 and i.find("@") == -1
    if is_a_command(command):
        s['instruction_type'] = 'A'
        if command.startswith('@'):
            value = command[1:]
            if value.isdigit():
                s['value'] = value
                s['value_type'] = 'NUMERIC'
                s['dest'] = ''
                s['comp'] = ''
                s['jmp'] = ''
            else:
                if is_valid_symbol(value):
                    s['value'] = value
                    s['value_type'] = 'SYMBOL'
                    s['dest'] = 'null'
                    s['comp'] = ''
                    s['jmp'] = 'null'
                else:
                    s['status'] = -1
        else:
            s['status'] = -1
    elif is_c_command(command):
        s['instruction_type'] = 'C'
        s['value']=''
        s['value_type']=''
        semi = command.find(';')
        equa = command.find('=')
        if equa != -1 and semi != -1: #dest=comp;jump
            s['dest'] = command[:equa]
            s['comp'] = command[equa+1:semi]
            s['jmp']  = command[semi+1:]
        if equa == -1 and semi != -1: #comp;jump
            s['dest'] ='null'
            s['comp'] = command[:semi]
            s['jmp']  = command[semi+1:]
        if equa != -1 and semi == -1: #dest=comp
            s['dest'] = command[:equa]
            s['comp'] = command[equa+1:]
            s['jmp']  = 'null'
        if s['dest'] not in valid_dest_patterns or s['comp'] not in valid_comp_patterns or s['jmp'] not in valid_jmp_patterns:
            s['status'] = -1
    elif is_l_command(command):
        s['instruction_type'] = 'L'
        if command.startswith('(') and command.endswith(')'):
            label = command[1:-1].strip()  # Extract the label name
            s['value'] = label
        else:
            s['status'] = -1
    else:
        if command.startswidth('//') or command == '\n' or command == '':
            pass
        else:
            s['status'] = -1
    
    if s['status'] == -1:
        s['instruction_type'] = ''
        s['value'] = ''
        s['value_type'] = ''
        s['dest'] = ''
        s['comp'] = ''
        s['jmp'] = ''
    return s
   
def generate_machine_code():
    """Generate machine code from intermediate data structure"""
    
    machine_code = []
    
    return machine_code
    

def print_machine_code(machine_code):
    """Print generated machine code"""
    
    rom_address = 0
    for code in machine_code:
        print(rom_address, ':', code)
        rom_address = rom_address + 1


def add_entry(symbol, address):
        valid_symbol_table[symbol] = address
        
def get_address(symbol):
    if symbol not in valid_symbol_table:
        return symbol
    else:
        return valid_symbol_table[symbol]

def gen_a(addr):
   return '0' + bits(addr).zfill(15)

def dest( d):
    return (valid_dest_patterns[d])

def comp( c):
   return valid_comp_patterns[c]

def jump( j):
    return (valid_jmp_patterns[j])

def bits( n):
        return bin(int(n))[2:]

def run_assembler(file_name):      
    """Pass 1: Parse the assembly code into an intermediate data structure.
    The intermediate data structure can be a list of elements, called ir, where 
    each element is a dictionary with the following structure: 
    
    s['instruction_type'] = ''
    s['value'] = ''
    s['value_type'] = ''
    s['dest'] = ''
    s['comp'] = ''
    s['jmp'] = ''
    s['status'] = 0
    
    The symbol table is also generated in this step.    
    """
    cur_addr = 0
    ram_addr = 1024
    # FIXME: Implement Pass 1 of the assembler to generate the intermediate data structure
    # First pass: determine memory locations of label definitions: (LABEL)
    with open(file_name, 'r') as f:
        for command in f:  
            cmd = parse(command)
            if cmd['instruction_type'] == 'C' or cmd['instruction_type'] == 'A':
                cur_addr +=1 
            elif cmd['instruction_type'] == 'L':
                add_entry(cmd['value'],cur_addr)
                
    # FIXME: Implement Pass 2 of assembler to generate the machine code from the intermediate data structure
    machine_code = []
    with open(file_name, 'r') as f:
        for command in f:
            cmd_1 = parse(str(command))
            # print(command)
            # print(cmd_1)
            out_l = ''
            if cmd_1['instruction_type'] == 'A':
                out_l = '0'
                if cmd_1['value_type'] == 'SYMBOL':
                    if cmd_1['value'] in valid_symbol_table:
                        var_addr = valid_symbol_table[cmd_1['value']]
                        out_l = out_l + format(var_addr, 'b').zfill(15)
                    else:
                        valid_symbol_table[cmd_1['value']] = ram_addr
                        out_l = out_l + format(ram_addr,'b').zfill(15)
                        ram_addr += 1
                elif cmd_1['value_type'] == 'NUMERIC':
                    out_l = out_l + format(int(cmd_1['value']),'b').zfill(15)
                machine_code.append(out_l)
            elif cmd_1['instruction_type'] == 'C':
                out_l = '111'
                out_l = out_l + comp(cmd_1['comp']) + dest(cmd_1['dest']) + jump(cmd_1['jmp'])
                machine_code.append(out_l)

    return machine_code
    
  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python assembler.py file-name.asm")
        print("Example: Python assembler.py mult.asm")
    else:
        print("Assembling file:", sys.argv[1])
        print()
        file_name_minus_extension, _ = os.path.splitext(sys.argv[1])
        output_file = file_name_minus_extension + '.hack'
        machine_code = run_assembler(sys.argv[1])
        if machine_code:
            print('Machine code generated successfully');
            print('Writing output to file:', output_file)
            f = open(output_file, 'w')
            for s in machine_code:
                f.write('%s\n' %s)
            f.close()
        else:
            print('Error generating machine code')
            