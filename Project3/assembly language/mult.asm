// mult.asm
// Calculate C = A * B

// set value at R18 = 0
@18
M=0
// load value of R17 to D-register
@17
D=M
//if B <0, exit
@END
D;JEQ
//Start loop
(LOOP)
//Load value A of R16 to D-register
@16
D=M
// Add value C = C + A to R18
@18
M=M+D
// Minus value B of R17 by 1
@17
D=M
D=D-1
M=D
//Back to loop again
@LOOP
D;JGT // Check the new value of B

(END)
@END
0;JMP