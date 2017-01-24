import time

from environment import Environment
from exceptions import ParsingError, SimulationError
from instructions import EmptyInstruction, LoadInstruction, StoreInstruction, BranchInstruction


def build_instruction(tokens, line_number, labels):
    if len(tokens) == 0:
        return EmptyInstruction(tokens, line_number)

    operator = tokens[0]
    operands = tokens[1:]
    inst = None
    if operator == "LD":
        inst = LoadInstruction(operands, line_number)
    elif operator == "ST":
        inst = StoreInstruction(operands, line_number)
    elif operator == "BR":
        inst = BranchInstruction(operands, line_number, labels)

    return inst


class Simulator:
    instructions = []
    labels = {}

    def __init__(self, lines):
        # Data to help the parsing
        valid_instructions = set(["LD", "ST", "BR"])

        # Tokenize all the instructions
        dirty_instructions = []
        for line in lines:
            # Replace a comment by an empty line
            if len(line) > 0 and line[0] == "#":
                dirty_instructions.append([])
            else:
                dirty_instructions.append(line.split())

        # Prepare the instructions
        for line_number, instruction in enumerate(dirty_instructions):
            line_number += 1  # Line number start at 1
            nb_labels = 0
            for index, token in enumerate(instruction):
                # First identify all the labels and remove them
                if token[-1:] == ":":
                    label = token[:-1]
                    if not label.isalpha():
                        raise ParsingError("«" + label + "» is not a valid label at line " + str(line_number))

                    if label in self.labels:
                        raise ParsingError("«" + label + "» is duplicated at line " + str(line_number))

                    self.labels[label] = line_number
                    nb_labels += 1
                else:
                    break

            # Check that the remaining tokens don't contains labels
            for index, token in enumerate(instruction[nb_labels:]):
                if token[-1:] == ":":
                    raise ParsingError("Unexpected label encountered at line " + str(line_number))

            # Remove the labels from the dirty instructions
            dirty_instructions[line_number - 1] = instruction[nb_labels:]

        # Now that the labels are known, build all the instruction
        for line_number, instruction in enumerate(dirty_instructions):
            line_number += 1  # Line number start at 1

            # Check the validity of instructions
            if len(instruction) > 0 and instruction[0] not in valid_instructions:
                raise ParsingError("Invalid instruction «" + instruction[0] + "» found at line " + str(line_number))

            # Build the instruction itself
            inst = build_instruction(instruction, line_number, self.labels)
            self.instructions.append(inst)

    def simulate(self, max_time):
        # Prepare the environment for the simulation
        environment = Environment(5, 256)

        start_time = time.time()

        try:
            # Execute the simulation
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    raise SimulationError("Maximum time allowed for the simulation exceeded!")

                # Prepare the next instruction (Jump instructions can overwrite this value)
                environment.next_instruction = environment.current_instruction + 1

                # Check if the simulation is over
                if environment.current_instruction >= len(self.instructions):
                    break

                # Do the instruction logic
                inst = self.instructions[environment.current_instruction]
                inst.simulate(environment)

                # Jump to the next instruction
                environment.current_instruction = environment.next_instruction
        except SimulationError as error:
            message, = error.args
            raise SimulationError(message + " occurred at line " + str(environment.current_instruction+1))

        # Print the finale results
        environment.print()
