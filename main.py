from automaton import *
from intersection import *
from union import *
from optimize import *
from basic_automata import *

a=exists(exists(intersection(succ('Y','X'), sub('Y','X')), 'Y'), 'X')
write_to_gv(a, "graph.gv")

a=exists(exists(exists(intersection(intersection(succ('Y','X'), succ('Z','Y')), sub('Z', 'X')), 'Z'), 'Y'), 'X')
write_to_gv(a, "graph.gv")
