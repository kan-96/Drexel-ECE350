// sys.vm
// function [funtion_name] [nvars]
// Push nvars local variables into the stack
@SP
A=M
M=0
@SP
M=M+1 // push 0
@256
D=A
@SP
M=D
// call function_name n_args
// Push return address to stack
@main$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
// Push LCL
@LCL
D=M
@SP
A=M
M=D
M=D
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
// Set LCL register to current SP
@SP
D=M
@LCL
M=D
// Generate goto code
// (return-address)
(main$ret.3)
(THATS_ALL_FOLKS)
@THATS_ALL_FOLKS
0;JMP
