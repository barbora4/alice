from automaton import *
from intersection import *
from union import *
from optimize import *
from basic_automata import *
from parser import *

a=parse("formulas/f.fl")
write_to_gv(a, "graph.gv")
