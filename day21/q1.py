import re


def main():

    fileData = readFiles()

    ipReg, program = parseProgram(fileData)

    reg = runProgram(ipReg, program)


def runProgram(ipReg, program):

    # Initial registers
    reg = [0] * 6
    reg[0] = 16128384
    print('r0:', reg[0])

    # Run program when instruction pointer is not over program length
    while(reg[ipReg] < len(program)):

        # Get instruction
        instr = program[reg[ipReg]]

        # Execute instruction
        globals()[instr['op']](reg, instr)

        # Increment instruction pointer
        reg[ipReg] += 1

        """
        Program only halts when program hits line 28 and r0 == r4.
        r0 never changes throughout program run.
        Run program and look at registers when program hits line 28.
        """
        if reg[ipReg] == 28:
            print(reg)

    return reg


def parseProgram(fileData):
    ipData = fileData[0]
    programData = fileData[1:]

    # Get instruction pointer register
    ipPattern = re.compile(r'\#ip (\d)')
    ipReg = ipPattern.match(ipData).groups()[0]
    ipReg = int(ipReg)

    # Parse program
    program = list(map(lambda d: toInstrType(d), programData))

    return ipReg, program


def toInstrType(d):
    # Convert instruction text to instruction data structure
    instruction = d.split(' ')
    instruction = {
        'op': instruction[0],
        'A': int(instruction[1]),
        'B': int(instruction[2]),
        'C': int(instruction[3]),
    }

    return instruction


"""
Instruction operation functions
"""

def addr(reg, instr):
    reg[instr['C']] = reg[instr['A']] + reg[instr['B']]
    return reg


def addi(reg, instr):
    reg[instr['C']] = reg[instr['A']] + instr['B']
    return reg


def mulr(reg, instr):
    reg[instr['C']] = reg[instr['A']] * reg[instr['B']]
    return reg
    

def muli(reg, instr):
    reg[instr['C']] = reg[instr['A']] * instr['B']
    return reg


def banr(reg, instr):
    reg[instr['C']] = reg[instr['A']] & reg[instr['B']]
    return reg
    

def bani(reg, instr):
    reg[instr['C']] = reg[instr['A']] & instr['B']
    return reg


def borr(reg, instr):
    reg[instr['C']] = reg[instr['A']] | reg[instr['B']]
    return reg
    

def bori(reg, instr):
    reg[instr['C']] = reg[instr['A']] | instr['B']
    return reg


def setr(reg, instr):
    reg[instr['C']] = reg[instr['A']]
    return reg
    

def seti(reg, instr):
    reg[instr['C']] = instr['A']
    return reg


def gtir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] > reg[instr['B']] else 0
    return reg


def gtri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > instr['B'] else 0
    return reg


def gtrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > reg[instr['B']] else 0
    return reg


def eqir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] == reg[instr['B']] else 0
    return reg


def eqri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == instr['B'] else 0
    return reg


def eqrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == reg[instr['B']] else 0
    return reg


def readFiles():
    data = []
    file = open('input.txt', 'r')
    data = file.read().split('\n')[:-1]
    file.close()
    return data


if __name__ == '__main__':
    main()
