from automaton import *
from intersection import *
from union import *
from optimize import *
from basic_automata import *

a=exists(exists(intersection(succ('Y','X'), sub('Y','X')), 'Y'), 'X')
write_to_gv(a, "graph.gv")

a=intersection(succ('Y','X'), succ('Z', 'Y'))
write_to_gv(a,"graph.gv")
print(a.states)

a=intersection(intersection(succ('Y','X'), succ('Z', 'Y')), sub('Z', 'X'))
write_to_gv(a, "graph.gv")
print(a.states)

with open("automata/a.ba") as f:
    a=load_data(f)
with open("automata/a.ba") as f:
    b=load_data(f)

d=intersection(a,b)
write_to_file(d, "pokus")
