from abc import abstractmethod

from exceptions import ParsingError, SimulationError


class Instruction:
    nb_operands = -1;
    operands = []
    line_number = -1;

    def __init__(self, operands, line_number):
        self.operands = operands
        self.line_number = line_number

        if len(operands) != self.nb_operands:
            raise ParsingError("Unexpected number of operands at line " + str(self.line_number))

    @abstractmethod
    def simulate(self, environment):
        pass


class EmptyInstruction(Instruction):
    nb_operands = 0;

    def simulate(self, environment):
        # Do nothing
        pass

    def __init__(self, operands, line_number):
        Instruction.__init__(self, operands, line_number)


class LoadInstruction(Instruction):
    nb_operands = 2;

    def simulate(self, environment):

        # Get the value to load into the register
        value = self.operands[1]
        if value[0] == "#":
            value = int(value[1:])
        elif value[0] == "R":
            ndx = environment.locate_register(self.operands[1])
            value = environment.registers[ndx]
        else:
            load_location = environment.locate_memory(value, False)
            value = environment.memory[load_location]

        # Get the correct register
        register_index = environment.locate_register(self.operands[0])

        # Load the value
        environment.registers[register_index] = value

    def __init__(self, operands, line_number):
        Instruction.__init__(self, operands, line_number)


class StoreInstruction(Instruction):
    nb_operands = 2;

    def simulate(self, environment):
        store_location = environment.locate_memory(self.operands[0], True)

        value = self.operands[1]
        if value[0] == "#":
            value = int(value[1:])
        else:
            ndx = environment.locate_register(self.operands[1])
            value = environment.registers[ndx]

        environment.memory[store_location] = value

    def __init__(self, operands, line_number):
        Instruction.__init__(self, operands, line_number)


class BranchInstruction(Instruction):
    nb_operands = 1;
    target_label = None
    target_ln = -1

    def simulate(self, environment):
        # Jump to the label
        environment.next_instruction = self.target_ln
        pass

    def __init__(self, operands, line_number, labels):
        Instruction.__init__(self, operands, line_number)

        if operands[0] not in labels:
            raise ParsingError("Label not found at line " + str(self.line_number))

        self.target_label = operands[0]
        self.target_ln = labels[self.target_label]