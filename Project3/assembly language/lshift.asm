// lshift.asm

    // reset value of R[19]
    @19
    M=0
    //Check the sign of A
    @16
    D=M
    @1  //Save value of A to R[1] for furture use
    M=D
    // Checkif A of R[16] is negative number
    @NEGATIVE_CHECK
    D;JLT
    @19
    M=0
(NEGATIVE_CHECK_END)
    //Load value of s, and check if s is valid number
    @17
    D=M
    @END
    D;JEQ

//Start loop
(LOOP)
    //Load new value of A
    //set value of R18 to 0
    @18
    M=0
    @16           // Load value of A, and then 'new A'
    D=M
    @18
    M=M+D         //Time once
    @18
    M=M+D         //Time twice, and save new vale for result
    D=M
    @16            
    M=D           // save the new value of 'A' to get ready for next round
    @17           // minus s by 1, keep track of shift
    D=M
    D=D-1
    M=D
    @LOOP
    D;JGT //Check new value of s>0

    //if A is negative signed, R[19] = 1
    @19
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
(NEGATIVE_CHECK)
    @19
    M=1
    @16
    D=-M
    M=D
    @NEGATIVE_CHECK_END
    0;JMP