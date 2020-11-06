from sys import stdin
from automaton import *
from parser import *

a=parse(stdin)
write_to_gv(a, "graph.gv")
write_to_file(a, "a.ba")
