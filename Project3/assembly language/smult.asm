// smult.asm
// Calculate C = A * B

//RAM[16] store value of A
//RAM[17] store value of B
//RAM[18] store the result
//RAM[19] store the sign of result

    @18     // set value at R18 = 0
    M=0
    @19     // set value at R19 = 1 
    M=0

    //Load value of A and check for negative sign
    @16
    D=M
    @NEGATIVE_CHECK_1
    D;JLT
(NEGATIVE_CHECK_1_END)

    // load value of R17 to D-register
    @17
    D=M
    @NEGATIVE_CHECK_2
    D;JLT
(NEGATIVE_CHECK_2_END)

    //if B <0, exit
    @17
    D=M
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
    D;JGT       // Check the new value of B
    @19         // Check the sign of result
    D=M
    @NEGATIVE_OUTPUT
    D;JGT

(END)
    @END
    0;JMP

    //check negative
(NEGATIVE_OUTPUT)
    @18
    D=-M
    M=D
    @END
    0;JMP

    //Place R[19]= 1 if A is negative, and A = -A
(NEGATIVE_CHECK_1)
    @19
    M=-M                // 0 -> 0, 1->-1
    M=M+1               // 0 -> 1, -1 -> 0
    @16
    D=-M
    M=D
    @NEGATIVE_CHECK_1_END
    0;JMP

(NEGATIVE_CHECK_2)
    @19
    M=-M                // 0 -> 0, 1->-1
    M=M+1               // 0 -> 1, -1 -> 0
    @17
    D=-M
    M=D
    @NEGATIVE_CHECK_2_END
    0;JMP