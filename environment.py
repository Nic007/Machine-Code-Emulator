import numpy

from exceptions import SimulationError


class Environment:
    # Instructions data
    current_instruction = 0
    next_instruction = 0

    # Registers data
    nb_registers = 0
    registers = []

    # Memory data
    memory_size = 0
    memory = []
    variables = {}

    __bloc_size__ = 32

    def __init__(self, nb_registers, memory_size):

        self.nb_registers = nb_registers
        self.registers = [0 for _ in range(nb_registers)]

        # Special contraint to be able to print memory
        if memory_size % self.__bloc_size__ != 0:
            raise ValueError("Memory size must be a multiple of " + str(self.__bloc_size__))
        self.memory_size = memory_size
        self.memory = [0 for _ in range(self.memory_size)]

    def locate_memory(self, operand, can_create_variable):
        # Try to get the memory adress

        # First method, it's simply a variable
        if operand.isalpha():
            # We are directly accessing a variable and we can create: we are probably in a store
            if operand not in self.variables:
                if not can_create_variable:
                    raise SimulationError("The variable «" + operand + "» cannot be found!")
                elif len(self.variables) == self.memory_size:
                    raise SimulationError("The maximum number of variables has been reached!")
                self.variables[operand] = len(self.variables)

            return self.variables[operand]

    def locate_register(self, operand):
        register_index = operand
        if register_index[0] != "R" and len(register_index) < 2:
            raise SimulationError("«" + operand + "» is not a valid register")

        register_index = int(register_index[1:])
        if register_index < 0 or register_index >= self.nb_registers:
            raise SimulationError("«" + operand + "» is out of bound")

        return register_index

    def print(self):
        print("\nState of simulation: ")
        print("Registers: " + str(self.registers))

        print("\nMemory:")
        row_size = self.__bloc_size__
        column_size = int(self.memory_size / row_size)

        matrix = numpy.reshape(self.memory, (column_size, row_size))
        print(matrix)
