// sys.vm
// function init 0
(init)
// Push nvars local variables into the stack
@256
D=A
@SP
M=D
// call main 0
// Push return address to stack
@LABEL3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
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
// ARG = SP-5-n
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
// goto main
@main
0;JMP
// (return-address)
(LABEL3)
(WHILE)
// goto [label]
@WHILE
0;JMP
