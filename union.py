"""Union of two Buchi automata."""

from itertools import product
from copy import copy 
from automaton import *
from atomic_automata import cylindrification
from optimize import optimize

def union(a1,a2):
    """Algorithm for union of two Buchi automata."""
    
    # add all variables to input alphabet and transitions
    cylindrification(a1,a2)

    # don't do any algorithm for two same automata
    if a1==a2:
        return a1

    start = {"S"}         # new start state
    
    # unique name for every state
    states = set()
    for s in a1.states:
        states.add((s,'1'))
    for s in a2.states:
        states.add((s,'2'))
    for s in start:
        states.add(s)
    
    alphabet = a1.alphabet|a2.alphabet
    
    transitions=set()
    for t in a1.transitions:
        transitions.add(((t[0],'1'),t[1],(t[2],'1')))
    for t in a2.transitions:
        transitions.add(((t[0],'2'),t[1],(t[2],'2')))

    accept = set()
    for s in a1.accept:
        accept.add((s,'1'))
    for s in a2.accept:
        accept.add((s,'2'))

    # add transitions from new start state
    old_transitions=copy(transitions)
    old_start=set()
    for s in a1.start:
        old_start.add((s,'1'))
    for s in a2.start:
        old_start.add((s,'2'))
    
    for t in old_transitions:
        if t[0] in old_start:
            for s in start:
                transitions.add((s,t[1],t[2]))
            
            if not any(i[0]==t[0] and i[0]==i[2] for i in old_transitions):
                # remove old start states without self loop
                transitions.remove(t)
            elif t[0]==t[2]:
                # old start state with self loop won't be removed
                for s in start:
                    transitions.add((s,t[1],t[2]))

            # if one of the old start states was accepting, the new one will be as well
            if t[0] in accept:
                for s in start:
                    accept.add(s)

    # remove old start states
    for s in copy(start):
        if not any(t[0] in states or t[2] in states for t in transitions):
            states.remove(s)

    # remove accept states
    for s in copy(accept):
        if s not in states:
            accept.remove(s)

    transitions=list(transitions)
    for i in range(len(transitions)):
        transitions[i]=list(transitions[i])

    a=Automaton(states,alphabet,transitions,start,accept)
    
    optimize(a)
   
    # edit names of states and transitions
    edit_names(a)  
    edit_transitions(a)

    return a
