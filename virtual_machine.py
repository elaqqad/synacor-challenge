"""Module implementing the virtual machine"""
import sys
import itertools
from array import array
from collections import defaultdict
from dumper import Dumper
MAX_ADDRESS = 32768


class RuntimeException(Exception):
    """ This exception is raised when we encounter a runtime error
    """
    pass

class VirtualMachineMemory:
    """ Virtual machine memory (Both registers and normal memory)
    """
    def __init__(self):
        self.registers = array('H', [0, 0, 0, 0, 0, 0, 0, 0])
        self.memory = array('H', itertools.repeat(0, 0x10000))

    def __getitem__(self, address):
        if 0 <= address < MAX_ADDRESS:
            return self.memory[address]
        elif MAX_ADDRESS <= address < MAX_ADDRESS + 8:
            return self.registers[address - MAX_ADDRESS]
        else:
            raise RuntimeException(f"Address {address} is invalid")

    def __setitem__(self, address, value):
        if 0 <= address < MAX_ADDRESS:
            self.memory[address] = value % MAX_ADDRESS
        elif MAX_ADDRESS <= address < MAX_ADDRESS + 8:
            self.registers[address - MAX_ADDRESS] = value % MAX_ADDRESS
        else:
            raise RuntimeException(f"Address {address} is neither memory nor register")

    def value(self, address):
        """ Returns the value of a register or keep as is if < 2^15

        Args:
            address (int): address satisfying 0 <= start < 2**15 + 8

        Raises:
            RuntimeException: if the above condition is not satisfied

        Returns:
            int : the value at given register or address.
        """
        if 0 <= address < MAX_ADDRESS:
            return address
        elif MAX_ADDRESS <= address < MAX_ADDRESS + 8:
            return self.registers[address - MAX_ADDRESS]
        else:
            raise RuntimeException(f"Value {address} is invalid as a number or a register")

    def code_of(self, address):
        """ Name of the register for code dumping

        Args:
            address (int): address satisfying 0 <= start < 2**15 + 8

        Raises:
            RuntimeException: if the above condition is not satisfied
            
        Returns:
            string : value of the address (int or r*)
        """
        codes = ['ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh']
        if 0 <= address < MAX_ADDRESS :
            return str(address)
        if MAX_ADDRESS <= address < MAX_ADDRESS + 8:
            return codes[address - MAX_ADDRESS].lower()
        raise RuntimeException(f"Value {address} is invalid as a number or a register")

    def read(self, start, length):
        """ Read the values of a range starting at start with given length

        Args:
            start (int): start address satisfying 0 <= start < 2**15 + 8
            length (int): length of the range to read

        Returns:
            array : a sub array containing the values
        """
        return self.memory[start:start + length]


class VirtualMachineStack:
    """ Simple stack class
    """
    def __init__(self):
        self.stack = array('H')

    def push(self, value):
        """ Push a value to the stack

        Args:
            value (int): value to push
        """
        self.stack.append(value)

    def pop(self):
        """ Pops a value from the stack

        Returns:
            int : the popped value
        """
        return self.stack.pop()


class VirtualMachine:
    """ VirtualMachine
    """
    def __init__(self, player):
        self.player = player
        self.hacks = defaultdict(list)
        self.memory = VirtualMachineMemory()
        self.stack = VirtualMachineStack()
        self.call_stack = []
        self.cursor = 0
        self.instructions = {
            0 : ('halt', 0),
            1 : ('set ', 2),
            2 : ('push', 1),
            3 : ('pop ', 1),
            4 : ('eq  ', 3),
            5 : ('gt  ', 3),
            6 : ('jmp ', 1),
            7 : ('jt  ', 2),
            8 : ('jf  ', 2),
            9 : ('add ', 3),
            10: ('mult', 3),
            11: ('mod ', 3),
            12: ('and ', 3),
            13: ('or  ', 3),
            14: ('not ', 2),
            15: ('rmem', 2),
            16: ('wmem', 2),
            17: ('call', 1),
            18: ('ret ', 0),
            19: ('out ', 1),
            20: ('in  ', 1),
            21: ('noop', 0)
        }
        self.dumper = Dumper(self.memory, self.instructions)
    def load(self, filename):
        """ loads the given filename as a program into memory
        Args:
            filename (string): path to the program
        Returns:
            int : the size of the program
        """
        program = array('H')
        with open(filename, 'rb') as file:
            program.frombytes(file.read())
        self.memory.memory[0:len(program)] = program

    def run(self):
        """ Runs the virtual machine
        """
        while self.next():
            continue

    def hack(self, cursor, code) :
        """ Dangerous ! evaluates the given code when we visit the given cursor address

        Args:
            cursor (int): address to run code at
            code (string): code to run
        """
        self.hacks[cursor].append(code)

    def next(self):
        """ Reads and executes the next instruction
        """
        for hack in self.hacks[self.cursor]:
            #self.player.write(f"\nApplying hack, address = {self.cursor} : {hack}\n")
            eval(hack)
        instruction, args = self.next_instruction(self.cursor)
        do_instruction = getattr(self, f'do_{instruction}'.strip())
        self.cursor += 1 + len(args)
        return do_instruction(*args)

    def next_instruction(self, address):
        """ Reads the next instruction

        Args:
            address (int): address to start reading at

        Raises:
            RuntimeException: if the operation is not defined

        Returns:
            (string, array) : operation and argument values
        """
        instruction_code = self.memory[address]
        try:
            do_name, num_args = self.instructions[instruction_code]
        except KeyError as key_error:
            raise RuntimeException(f"Code {instruction_code} not defined") from key_error
        args = self.memory.read(address + 1, num_args)
        return do_name, args

    def do_halt(self):
        """ operation halt
        """
        return False

    def do_set(self, reg, value):
        """ operation set
        """
        self.memory[reg] = self.memory.value(value)
        return True

    def do_push(self, value):
        """ operation push
        """
        value = self.memory.value(value)
        self.stack.push(value)
        return True

    def do_pop(self, addr):
        """ operation pop
        """
        self.memory[addr] = self.stack.pop()
        return True

    def do_eq(self, a, b, c):
        """ operation eq
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = 1 if b == c else 0
        return True

    def do_gt(self, a, b, c):
        """ : operation gt
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = 1 if b > c else 0
        return True

    def do_jmp(self, addr):
        """ operation jmp
        """
        addr = self.memory.value(addr)
        self.cursor = addr
        return True

    def do_jt(self, a, addr):
        """ operation jt
        """
        a = self.memory.value(a)
        addr = self.memory.value(addr)
        if a:
            self.cursor = addr
        return True

    def do_jf(self, a, addr):
        """ operation jf
        """
        a = self.memory.value(a)
        addr = self.memory.value(addr)
        if a == 0:
            self.cursor = addr
        return True

    def do_add(self, a, b, c):
        """ operation add
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = b + c
        return True

    def do_mult(self, a, b, c):
        """ operation mult
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = b * c
        return True

    def do_mod(self, a, b, c):
        """ operation mod
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = b % c
        return True

    def do_and(self, a, b, c):
        """ operation and
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = b & c
        return True

    def do_or(self, a, b, c):
        """ operation or
        """
        b = self.memory.value(b)
        c = self.memory.value(c)
        self.memory[a] = b | c
        return True

    def do_not(self, a, b):
        """ operation not
        """
        b = self.memory.value(b)
        self.memory[a] = ~b
        return True

    def do_rmem(self, a, b):
        """ operation rmem
        """
        b = self.memory.value(b)
        self.memory[a] = self.memory[b]
        return True

    def do_wmem(self, a, b):
        """ operation wmem
        """
        a = self.memory.value(a)
        b = self.memory.value(b)
        self.memory[a] = b
        return True

    def do_call(self, addr):
        """ operation call
        """
        addr = self.memory.value(addr)
        self.call_stack.append(addr)
        self.stack.push(self.cursor)
        self.cursor = addr
        return True

    def do_ret(self):
        """ operation ret
        """
        self.call_stack.pop()
        self.cursor = self.stack.pop()
        return True

    def do_out(self, char):
        """ operation out
        """
        char = chr(self.memory.value(char))
        self.player.write(char)
        return True

    def do_in(self, addr):
        """ operation in
        """
        read = self.player.read()
        self.memory[addr] = ord(read)
        return True

    def do_noop(self):
        """ operation noop
        """
        return True


class RealPlayer:
    """ Play the game using console (stdin & stdout)
    """
    def hack(self, virtual_machine) :
        """ Allows code to be run at specific moments

        Args:
            virtual_machine (VirtualMachine): virtual machine
        """
        self.virtual_machine = virtual_machine
    def write(self, char):
        """ Displays character to the screen

        Args:
            char (string): one character to display
        """
        sys.stdout.write(char)

    def read(self):
        """ Reads one character from screen

        Returns:
           string : input character
        """
        char = sys.stdin.read(1)
        while char == "!":
            self.save_hack()
            char = sys.stdin.read(1)
        return char

    def save_hack(self) :
        """ Adds a hack to the virtual machine
        """
        [cursor, code] = sys.stdin.readline().strip().split(":",1)
        self.virtual_machine.hack(int(cursor), code)

class FilePlayer :
    """ Play the game using the commands from given file
    """
    def __init__(self):
        with open("Solution/solution.txt", "r") as file:
            self.instructions = file.read()
        self.cursor = 0

    def hack(self, virtual_machine) :
        """ Adds code to be run at specific moments

        Args:
            virtual_machine (VirtualMachine): virtual machine
        """
        with open("Solution/hacks.yml", "r") as file:
            for line in file.readlines():
                [cursor, code] = line.strip().split(":",1)
                virtual_machine.hack(int(cursor), code)
    def write(self, char):
        """ Displays a character to the screen

        Args:
            char (string): the character to display
        """
        sys.stdout.write(char)
    def read(self):
        """ Returns one character of current instruction
        """
        char = self.read_char()
        while char == "!":
            char = self.read_char()
        return char

    def read_char(self) :
        """ Reads one char
        """
        if self.cursor >= len(self.instructions):
            return sys.stdin.read(1)
        char = self.instructions[self.cursor]
        self.cursor = self.cursor + 1
        sys.stdout.write(char)
        return char

if __name__ == '__main__':
    player = FilePlayer()
    vm = VirtualMachine(player)
    player.hack(vm)
    vm.load("Program/challenge.bin")
    vm.run()
