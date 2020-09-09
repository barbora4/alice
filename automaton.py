"""Class Automaton, loading from .ba files and writing to them."""

import re
from dataclasses import dataclass

@dataclass
class Automaton:
    """Data class representing an automaton."""

    states: set
    alphabet: set
    transitions: set
    start: set
    accept: set

def load_data(file):
    """Loads data from .ba file to object Automaton"""

    start=set()         # start states
    transitions=set()   # transitions: [input, start, end]
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
                transitions.add((match.group(1), match.group(3), match.group(5)))
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

    return Automaton(states,alphabet,transitions,start,accept)


def write_to_file(a,f):
    with open(f, "w") as f:
        for i in a.start:
            f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))
        for i in a.transitions:
            f.write("{},[{},{},{}]->[{},{},{}]\n".format(i[1],i[0][0],i[0][1],i[0][2],i[2][0],i[2][1],i[2][2]))
        for i in a.accept:
            f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))

