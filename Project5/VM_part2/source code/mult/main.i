// main.vm
// function main 2
(main)
// Push nvars local variables into the stack
@SP
A=M
M=0
@SP
M=M+1 // push 0
@SP
A=M
M=0
@SP
M=M+1 // push 0
// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@LCL
D=M
@0
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push constant 5
@5
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@LCL
D=M
@1
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push local 0
@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 1
@LCL
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
// call mult 2
// Push return address to stack
@LABEL12
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
@2
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
// goto mult
@mult
0;JMP
// (return-address)
(LABEL12)
// Copy LCL to temp register R14 (FRAME)
@LCL
D=M
@R14
M=D // FRAME = LCL
@5
D=D-A
A=D
D=M
// Store return address in temp register R15 (RET)
@R15
M=D // RET = *(FRAME-5)
// Pop result from the working stack and move it to beginning of ARG segment
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R14
D=M-1
A=D
D=M
@THAT
M=D
@2
D=A
@R14
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@R14
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@R14
D=M-D
A=D
D=M
@LCL
M=D
@R15
A=M
0;JMP // goto RET
