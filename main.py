from sys import stdin
from automaton import *
from parser import *

file_text=stdin.read()
a=parse(file_text, analyse_predicates(file_text))

#write_to_gv(a, "graph.gv")
#write_to_file(a, "a.ba")

