from sys import stdin
from automaton import *
from parser import *
from optimize import *

file_text=stdin.read()
parse(file_text, analyse_predicates(file_text))

#with open("reduced_10_a.ba") as f:
#    a = load_data(f)

#edit_transitions(a)
#write_to_gv(a, "graph.gv")
#write_all_transitions(a)
#write_to_file(a, "a.ba")
