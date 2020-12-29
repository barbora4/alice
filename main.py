#! /usr/bin/python3
from sys import stdin
from automaton import *
from parser import *
from optimize import *
import os

file_text=stdin.read()
parse(file_text, analyse_predicates(file_text))

# reduce final automaton
stream = os.popen('java -jar ../RABIT250/Reduce.jar a.ba 10')
output = stream.read()
print(output)

# save automaton to a.ba
with open('reduced_10_a.ba') as f:
    a = load_data(f)
edit_transitions(a)
write_to_file(a, 'a.ba')
write_to_gv(a, 'graph.gv')

print(len(a.states))

# show automaton
os.popen('dot -Tpdf graph.gv -o graph.pdf')
os.popen('xdg-open graph.pdf')
