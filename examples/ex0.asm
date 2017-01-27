LD R0, #10
LD R1, #0
ST x, #1

label:
DEC R0
INC R1

BNETZ R0, label