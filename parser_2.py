#remove all white space

import os
import sys

def remove_whitespace(command):
    """Remove all whitespace from a given command."""
    return command.replace(" ", "")
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

# def parse(command):
#     """Implements finite automate to scan assembly statements and parse them.

#     WHITE SPACE: Space characters are ignored. Empty lines are ignored.
    
#     COMMENT: Text beginning with two slashes (//) and ending at the end of the line is considered 
#     comment and is ignored.
    
#     CONSTANTS: Must be non-negative and are written in decimal notation. 
    
#     SYMBOL: A user-defined symbol can be any sequence of letters, digits, underscore (_), dot (.), 
#     dollar sign ($), and colon (:) that does not begin with a digit.
    
#     LABEL: (SYMBOL)
#     """
    
#     # Data structure to hold the parsed fields for the command
#     s = {}
#     s['instruction_type'] = ''
#     s['value'] = ''
#     s['value_type'] = ''
#     s['dest'] = ''
#     s['comp'] = ''
#     s['jmp'] = ''
#     s['status'] = 0
    
#     # Valid operands and operations for C-type instructions
#     valid_operands = '01DMA'
#     valid_operations = '+-&|'
    
    
#     command = remove_whitespace(command)
#     is_l_command = lambda i : i.find('(') != -1 and i.find(')') != -1    
#     is_a_command = lambda i : i.find('@') != -1   
#     is_c_command = lambda i : i.find("(") == -1 and i.find("@") == -1
#     if is_a_command(command):
#         s['instruction_type'] = 'A'
#         if command.startswith('@'):
#             value = command[1:]
#             if value.isdigit():
#                 s['value'] = value
#                 s['value_type'] = 'NUMERIC'
#                 s['dest'] = ''
#                 s['comp'] = ''
#                 s['jmp'] = ''
#             elif value[1].isalpha():
#                 if (value.isalnum() or value in '_.$:') and all(char.islower() for char in value):
#                         s['value'] = value
#                         s['value_type'] = 'SYMBOL'
#                         s['dest'] = 'null'
#                         s['comp'] = ''
#                         s['jmp'] = 'null'
#                 else:
#                     s['status'] = -1
#             else:
#                 s['status'] = -1
#         else:
#             s['status'] = -1
#     elif is_c_command(command):
#         s['instruction_type'] = 'C'
#         s['value']=''
#         s['value_type']=''
#         semi = command.find(';')
#         equa = command.find('=')
#         if equa != -1 and semi != -1: #dest=comp;jump
#             s['dest'] = command[:equa]
#             s['comp'] = command[equa+1:semi]
#             s['jmp']  = command[semi+1:]
#         if equa == -1 and semi != -1: #comp;jump
#             s['dest'] ='null'
#             s['comp'] = command[:semi]
#             s['jmp']  = command[semi+1:]
#         if equa != -1 and semi == -1: #dest=comp
#             s['dest'] = command[:equa]
#             s['comp'] = command[equa+1:]
#             s['jmp']  = 'null'
#         if s['dest'] not in valid_dest_patterns or s['comp'] not in valid_comp_patterns or s['jmp'] not in valid_jmp_patterns:
#             s['status'] = -1
#     elif is_l_command(command):
#         s['instruction_type'] = 'L'
#         if command.startswith('(') and command.endswith(')') and all(char.isupper() for char in command[1:-1]):
#             label = command[1:-1].strip()  # Extract the label name
#             s['value'] = label
#         else:
#             s['status'] = -1
#     else:
#         s['status'] = -1
    
#     if s['status'] == -1:
#         s['instruction_type'] = ''
#         s['value'] = ''
#         s['value_type'] = ''
#         s['dest'] = ''
#         s['comp'] = ''
#         s['jmp'] = ''
#     return s

# command1 = "@100"
# parsed1 = parse(command1)
# print(parsed1)