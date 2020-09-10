"""Union of two Buchi automata."""

from itertools import product
from copy import copy 
from automaton import Automaton

def union(a1,a2):
    """Algorithm for union of two Buchi automata."""
    
    start = '0'     # new start state
    states = a1.states|a2.states
    states.add(start)
    alphabet = a1.alphabet|a2.alphabet
    transitions = copy(a1.transitions|a2.transitions)
    accept = a1.accept|a2.accept

    # add transitions from new start state
    for t in a1.transitions|a2.transitions:
        if t[0] in a1.start|a2.start:
            transitions.add((start,t[1],t[2]))
            
            if not any(i[0]==t[0] and i[0]==i[2] for i in a1.transitions|a2.transitions):
                transitions.remove(t)
            elif t[0]==t[2]:
                # old start state with self loop won't be removed
                transitions.add((start,t[1],t[2]))

            # if one of the old start states was accepting, the new one will be as well
            if t[0] in accept:
                accept.add(start)

    # remove old start states
    for s in a1.start|a2.start:
        if not any(t[0] in states or t[2] in states for t in transitions):
            states.remove(s)

    # remove accept states
    for s in copy(accept):
        if s not in states:
            accept.remove(s)

    return Automaton(states,alphabet,transitions,start,accept)
