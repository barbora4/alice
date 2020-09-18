"""Class Automaton, loading from .ba files and writing to them."""

import re
import csv
from copy import copy
from dataclasses import dataclass

@dataclass
class Automaton:
    """Data class representing an automaton."""

    states: set
    alphabet: set
    transitions: list
    start: set
    accept: set

def load_data(file):
    """Loads data from .ba file to object Automaton."""

    start=set()         # start states
    transitions=list()  # transitions: [input, start, end]  
    accept=set()        # accept states
    alphabet=set()      # set of all input symbols
    states=set()        # set of all states

    beginning=True      
    
    for line in file:
        # start states
        if re.search(r"^\[(.)+\]\n$", line) and beginning:
            start.add(line[1:-2])
            states.add(line[1:-2])

        else:
            match=re.search(r"^((.)+),\[((.)+)\]->\[((.)+)\]\n$", line)
            # transitions
            if match:
                beginning=False
                transitions.append([match.group(3), match.group(1), match.group(5)]) 
                alphabet.add(match.group(1))
                states.add(match.group(3))
                states.add(match.group(5))
        
            # accept states
            elif re.search(r"^\[(.)+\]\n$", line) and not beginning:
                accept.add(line[1:-2])
                states.add(line[1:-2])

            # wrong file format
            else:
                raise SyntaxError("Wrong format!")

    return Automaton(states,alphabet,transitions,start,accept)


def write_to_file(a,f):
    """Writes automaton to .ba file."""

    with open(f, "w") as f:
        for i in a.start:
            if type(i)==tuple:
                f.write('[{}]\n'.format(','.join(map(str,i))))
            else:
                f.write('[{}]\n'.format(i))
        for i in a.transitions:
            if type(i[0])==tuple:
                t1='[%s]'%','.join(map(str, i[0]))
            else:
                t1="[{}]".format(i[0])
            if type(i[2])==tuple:
                t2='[%s]'%','.join(map(str, i[2]))
            else:
                t2="[{}]".format(i[2])
            f.write("{},{}->{}\n".format(i[1],t1,t2))
        for i in a.accept:
            if type(i)==tuple:
                f.write('[{}]\n'.format(','.join(map(str,i))))
            else:
                f.write('[{}]\n'.format(i))
 
def write_to_gv(a,f):
    """Writes automaton into .gv file."""

    with open(f, "w") as f:
        # beginning
        f.write("digraph finite_state_machine {\n")
        f.write("\trankdir=LR;\n")
        f.write('\tsize="8,5"\n')
        f.write("\tnode [shape = doublecircle];")
        for acc in a.accept:
            f.write(' {}'.format(''.join(map(str,acc)).replace(',','')))
        if len(a.accept)!=0:
            f.write(";\n")
        else:
            f.write("\n")
        if len(a.states)!=0:
            f.write('\tinit [label="", shape=point]\n')
        f.write("\tnode [shape = circle];\n")

        # states
        for s in a.states:
            f.write('\t{} [label="{}"];\n'.format(''.join(map(str,s)).replace(',',''), ','.join(map(str,s))))

        # transitions
        for s in a.start:
            f.write('\tinit -> {}\n'.format(''.join(map(str,s)).replace(',','')))
        for t in a.transitions:
            t0="{}".format(''.join(map(str,t[0])).replace(',',''))
            t2="{}".format(''.join(map(str,t[2])).replace(',',''))
            f.write('\t{} -> {} [ label = "{}" ];\n'.format(t0,t2,t[1]))

        # end
        f.write("}\n")


def edit_names(a):
    """Renames all states with numbers, starting with 0."""

    a.states=list(a.states)
    states=copy(a.states)
    for i in range(len(states)):
        # rename states in transitions
        for t in a.transitions:
            if t[0]==states[i]:
                t[0]=str(i)
            if t[2]==states[i]:
                t[2]=str(i)
        # rename start states
        a.start=list(a.start)
        for j in range(len(a.start)):
            if a.start[j]==states[i]:
                a.start[j]=str(i)
        a.start=set(a.start)
        # rename accept states
        a.accept=list(a.accept)
        for j in range(len(a.accept)):
            if a.accept[j]==states[i]:
                a.accept[j]=str(i)
        a.accept=set(a.accept)
        # rename state
        a.states[i]=str(i)
    a.states=set(a.states)
