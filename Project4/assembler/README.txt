# Hack Assembler

This Python script serves as an assembler for the Hack processor. It translates assembly code written in the Hack assembly language into machine code that the Hack computer can execute.

## Author

- **Original Author:** Naga Kandasamy
- **Date Created:** August 8, 2020
- **Date Modified (by student):** November 10, 2023
- **Student Name:** Khoa Nguyen

## Introduction

The assembler supports the translation of assembly commands into machine code for the Hack computer. It includes functionality for parsing, validating, and generating machine code from assembly instructions.

## Usage

To use the assembler, run the script from the command line with the following syntax:

```bash
python assembler.py file-name.asm
```

Replace `file-name.asm` with the path to your Hack assembly code file. For example:

```bash
python assembler.py mult.asm
```

## Features

### Supported Instructions

The assembler supports the following types of instructions:

1. **A-instructions:** Used for addressing constants and variables.
   - Example: `@123` or `@LOOP`

2. **C-instructions:** Used for computation and control.
   - Examples: `D=M`, `D+1`, `0;JMP`

3. **Label Definitions:** Used to define labels for branching and looping.
   - Example: `(LOOP)`

### Intermediate Representation

The assembler generates an intermediate representation for each assembly command, consisting of fields such as `instruction_type`, `value`, `value_type`, `dest`, `comp`, and `jmp`. This representation facilitates the translation process.

### Symbol Table

The assembler builds a symbol table that maps predefined symbols and labels to their respective memory locations.

## How It Works

1. **Pass 1: Label Definitions**
   - The assembler processes the input file to determine memory locations for label definitions.

2. **Pass 2: Generate Machine Code**
   - The assembler generates machine code based on the intermediate representation and the symbol table.

3. **Output**
   - The resulting machine code is written to a new file with a `.hack` extension.

## Additional Notes

- The assembler supports valid symbol patterns, constants, and predefined symbols according to the Hack assembly language specifications.

- The script includes functions for printing intermediate representations and machine code for debugging purposes.

## Example

```bash
python assembler.py sample.asm
```

This command assembles the `sample.asm` file and generates the corresponding machine code in `sample.hack`.

## Acknowledgments

- The original version of this script was authored by Naga Kandasamy.

Feel free to reach out for any additional support or feedback. Happy assembling!