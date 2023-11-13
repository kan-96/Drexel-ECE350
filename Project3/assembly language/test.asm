    @18 
    D=D+M           // Absolute address (base + index); our pointer value
    @19             // We store the first-pointer in RAM[19] for future use
    M=D
    @20             // We store the second-pointer in RAM[19] for future use
    M=D+1
    @19
    A=M             //Address register contains the first pointer
    D=M             // Load value of first-pointer to register
    @20
    A=M                 //Address register contains the second pointer
    D=D-M               // Load value A[i]-A[i-1]
    @20    // If value A[i] - A[i+1] > 0
    D;JGT               // Continue
    @IF_END               //Jump back the end of loop
    0;JMP