""" Module in order to dump the whole memory of the program"""
from array import array


class Dumper:
    """ Dumps the whole content of memory into a file
    """
    def __init__(self, memory, instructions):
        self.memory = memory
        self.instructions = instructions

    def write_code_to_file(self, start, end, filename):
        """ Writes code starting from start to end to a file in Dumps folder

        Args:
            start (int): start address
            end (int): end address
            filename (string): filename without extension, it will be created on Dumps folder.
        """
        with open(f"Dumps/{filename}.asm", 'w') as file:
            self.write_code_chunk(start, end, file)

    def write_code_chunk(self, start, end, file= None):
        """ Dumps the whole memory from start to end

        Args:
            start (int): start address
            end (int): end address
            file (TextIOWrapper, optional): file to write to. Defaults to None.
        """
        while start < end:
            (sec_name, is_data) = self.section_name(start)
            num_args = 0
            try:
                if not is_data :
                    operation_code = self.memory[start]
                    (line, num_args) = self.read_code(start, operation_code)
                    print(line.strip(), file = file)
                else :
                    print(self.read_data(start, sec_name).strip(), file = file)
            except IndexError:
                print(self.read_data(start, "data").strip(), file = file)
            except KeyError:
                print(self.read_data(start, "none").strip(), file = file)
            start = start + 1 + num_args

    def read_data(self, address, sec_name):
        """ Line of memory data with readable character if possible

        Args:
            address (int): address of memory content
            sec_name (string): name of the section

        Returns:
            string : the line to save to the file 
        """
        data = self.memory.memory[address]
        extra = "  ; " + repr(self.convert_to_char(data))
        line = self.format_line(address, sec_name, extra, f"{self.memory.code_of(data):<5}")
        return line

    def read_code(self, address, operation_code):
        """ Reads one line of code (op + args)

        Args:
            address (int): address of operation in memory
            instruction (string): name of the operation

        Returns:
            string : line of code
        """
        instruction, number_of_args = self.instructions[operation_code]
        args = self.memory.read(address + 1, number_of_args)
        extra = "  ; " + repr(self.convert_to_char(args[0])) if instruction == "out" else ""
        padded_args = " ".join(map(lambda a: f"{self.memory.code_of(a):<5}", args))
        line = self.format_line(address, instruction, extra, padded_args)
        return (line, number_of_args)

    def format_line(self, address, op_name, extra, padded_args):
        """ Formats the line by padding it left
        """
        return f"[{address:<5}] {op_name:<4} {str(padded_args):<25}{extra}"

    def section_name(self, address):
        """ Returns the section name in the code.

        Args:
            start (int): address in memory

        Returns:
            (string, bool): section name and whether it is definitely a data section
        """
        if 843 <= address < 845:
            return ("sec1", True)
        if 2317 <= address < 2734:
            return ("sec2", True)
        if 3945 <= address < 3958:
            return ("sec3", True)
        if 6068 <= address:
            return ("sec4", True)
        return ("", False)

    def write_memory_chunk(self, start, length):
        """ Prints to stdout the code starting at start with given length

        Args:
            start (int): start address
            length (int): length of section to print
        """
        data = self.memory.read(start, length)
        print(data)
        print(''.join(list(map(self.convert_to_char, data))))

    def convert_to_char(self, hex_value):
        """ Converts an ascii number to an ascii character

        Args:
            a (int): number between 0 and 256

        Returns:
            string : a readable valid ascii character or empty if not
        """
        try:
            result = chr(hex_value)
            if not result.isascii() or (hex_value not in [9,10,13] and 0 <= hex_value <= 31):
                return ''
            if self.is_special(result):
                return result
            if (result.isalpha() or result.isnumeric() or result.isspace()):
                return result
            return ''
        except:
            return ''

    def is_special(self, character):
        """ Checks if a character is special

        Args:
            character (string): character to check

        Returns:
            bool : True if the character is special otherwise False
        """
        return character in '+-?_!?=\/,;:*.@"&@()[]%<>\''

    def write_text_to_file(self, data, filename):
        """ Writes the whole data as a text file (Convert if possible)

        Args:
            data (array): data to dump to file
            filename (string): name of the file without the extension
        """
        with open(f"Dumps/{filename}.txt", 'w') as text_file:
            print(''.join(list(map(self.convert_to_char, data))), file = text_file)
