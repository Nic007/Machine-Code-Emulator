import os

from simulator import Simulator
from exceptions import ParsingError, SimulationError


def run_test(filename):
    with open(filename, 'r') as file:
        lines = list(file)

        try:
            simulator = Simulator(lines)
            simulator.simulate(5)  # Maximum of 5 seconds for the simulation
            print("Test of «" + filename + "» Succeeded")
        except ParsingError as error:
            print("Test of «" + filename + "» Failed: " + repr(error))
        except SimulationError as error:
            print("Test of «" + filename + "» Failed: " + repr(error))


# get all examples
for root, dirs, files in os.walk("examples/"):
    for file in files:
        if file.endswith(".asm"):
            run_test(os.path.join(root, file))
