// divide.asm
// Calculate C = A / B (integer division)

// Store A and B in memory locations RAM[16] and RAM[17]
// set value at R18 = 0
@18
M=0
// load value of R17 to D-register
@16
D=M
// Save value to random memory
@19
M=D
//if B <0, exit
@END
D;JEQ
//Start loop
(LOOP)
//Load value A of R16 to D-register
@17
D=M
@END
D;JEQ
// Add value C = C + A to R18
@18
M=M+1
// Minus value B of R17 by 1
@19
M=M-D
D=M
//Back to loop again
@LOOP
D;JGT // Check the new value of B
(END)
@END
0;JMP