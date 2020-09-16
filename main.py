from automaton import *
from intersection import *
from union import *
from optimize import *
from basic_automata import *

a=x_is_y('x','y')
write_to_gv(a,"graph.gv")

b=x_is_0('x')
a=union(a,b)
write_to_gv(a,"graph.gv")
