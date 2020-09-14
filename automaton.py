"""Class Automaton, loading from .ba files and writing to them."""

import re
import csv
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
    """Loads data from .ba file to object Automaton"""

    start=set()         # start states
    transitions=set()  # transitions: [input, start, end]  
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
                transitions.add((match.group(3), match.group(1), match.group(5))) 
                alphabet.add(match.group(1))
                states.add(match.group(3))
                states.add(match.group(5))
        
            # accept states
            elif re.search(r"^\[(.)+\]\n$", line) and not beginning:
                accept.add(line[1:-2])
                states.add(line[1:-2])

            # wrong file format
            else:
                raise FormatError("Wrong format!")

    return Automaton(states,alphabet,list(transitions),start,accept)


def write_to_file(a,f):
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
 
