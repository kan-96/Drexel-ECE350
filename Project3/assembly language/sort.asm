//sort.asm

// continue = 1;
// while (continue == 1) {
//  continue = 0;
//  for (i = 0; i < (n - 1); i++) {
//      if (A[i] > A[i + 1]) {
//          temp = A[i];
//          A[i] = A[i + 1];
//          A[i + 1] = temp;
//          /* We have exchanged elements. List is still unsorted and
//          additional pass may be required. */
//          continue = 1;
//      }
//   }
// }

// RAM[1] store continue value condition
// RAM[17] contains the number of elements in the array
// RAM[16] contain base address of the array A
// RAM[18] stores i
// RAM[19] Store address of first pointer
// RAM[20] Store address of second pointer
// RAM[21] Store a temp value

    @1         // RAM[1] store continue value condition
    M=1
    D=M
    @WHILE
    D;JGT
(WHILE)
    @1         // RAM[1] store continue value condition
    M=0
    @18         // RAM[18] stores i
    M = 0 // i = 0
    (LOOP)
        @17         // RAM[17] stores n
        D=M-1       // n-1
        @18         // RAM[18] stores i
        D=D-M       //(n-1) - i > 0
        @EXIT
        D;JEQ       // If(i-n+1) == 0 goto EXIT
        @16         // RAM[16] stores baes address of array A
        D=M
        @COMPARE_TWO
        0;JMP
        (COMPARE_TWO_END)
            @SWAP_VALUE
            0;JMP
            (SWAP_VALUE_END)
            @1         // RAM[1] store continue value condition
            M=1
            D=M
            @WHILE
            0;JMP
        (IF_END)
            @18          //RAM[18] stores i
            M=M+1        // i = i+1
            @LOOP        // Start a loop with new i
            0;JMP
(EXIT)
    @EXIT
    0;JMP

(COMPARE_TWO)
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
    @COMPARE_TWO_END    // If value A[i] - A[i+1] > 0
    D;JGT               // Continue
    @IF_END               //Jump back the end of loop
    0;JMP

//Swap two value
(SWAP_VALUE)
    @19
    A=M             //Address register contains the first pointer
    D=M             // Load value of first-pointer to register
    @21             //RAM 21 store temp value of A[I]
    M=D
    @20
    A=M             //Address register contains the second pointer
    D=M             // Load value of second-pointer to register
    @19
    A=M            //Address register contains the first pointe
    M=D            // Dereference pointer; store value in pointer location
    @21             //RAM 21 store temp value of A[i]
    D=M
    @20
    A=M             //Address register contains the second pointer
    M=D             // Load value of second-pointer to register
    @SWAP_VALUE_END
    0;JMP