"""Intersection of two Buchi automata"""

import itertools
from copy import copy
from automaton import *
from atomic_automata import cylindrification
from optimize import *

def intersection(a1,a2):
    """Algorithm for intersection of 2 Buchi automata."""

    # add all variables to input alphabet and transitions
    cylindrification(a1,a2)

    W=list(itertools.product(a1.start,a2.start,{'1'}))  # all reachable states
    Q=set()                                             # visited states  
    F=set()                                             # states [q1,q2,1] where q1 is accepting
    transitions=list()                                  # [state,input,next_state]   
    start=set(copy(W))

    # the construction for nfas can be applied if all the states of one of the two nbas are accepting
    nfa=all(q in a1.accept for q in a1.states) or all(q in a2.accept for q in a2.states)

    # algorithm for intersection of 2 Buchi automata
    for q in W:
        Q.add(q)
        if q[0] in a1.accept and q[2]=='1':
            F.add(q)
        for a in a1.alphabet|a2.alphabet:
            for t1 in a1.transitions:
                if input_equal(a,t1[1]) and t1[0]==q[0]: 
                    for t2 in a2.transitions:
                        if input_equal(a,t2[1]) and t2[0]==q[1]: 
                            
                            # if state of the 1st automaton in the 1st copy is not accepting, we stay in the 1st copy
                            if q[2]=='1' and q[0] not in a1.accept:
                                if [q,a,[t1[2],t2[2],'1']] not in transitions:
                                    transitions.append([q,a,[t1[2],t2[2],'1']]) 
                                if (t1[2],t2[2],'1') not in Q:
                                    W.append((t1[2],t2[2],'1'))
                            
                            # if state of the 1st automaton in the 1st copy is accepting, we move to the 2nd copy
                            if q[2]=='1' and q[0] in a1.accept:
                                if nfa:
                                    x='1'
                                else:
                                    x='2'
                                if [q,a,[t1[2],t2[2],x]] not in transitions:
                                    transitions.append([q,a,[t1[2],t2[2],x]])
                                if (t1[2],t2[2],x) not in Q:
                                    W.append((t1[2],t2[2],x))
                            
                            # if state of the 2nd automaton in the 2nd copy is not accepting, we stay in the 2nd copy
                            if q[2]=='2' and q[1] not in a2.accept:
                                if [q,a,[t1[2],t2[2],'2']] not in transitions:
                                    transitions.append([q,a,[t1[2],t2[2],'2']])
                                if (t1[2],t2[2],'2') not in Q:
                                    W.append((t1[2], t2[2],'2'))
                            
                            # if state of the 2nd automaton in the 2nd copy is accepting, we move to the 1st copy
                            if q[2]=='2' and q[1] in a2.accept:
                                if [q,a,[t1[2],t2[2],'1']] not in transitions:
                                    transitions.append([q,a,[t1[2],t2[2],'1']])
                                if (t1[2],t2[2],'1') not in Q:
                                    W.append((t1[2],t2[2],'1'))
    
    for t in transitions:
        t[2]=tuple(t[2])

    # creating set of accepting states
    accept=set()
    for s in W:
        if nfa:
            if s[0] in a1.accept and s[1] in a2.accept:
                accept.add(s)
        else:
            if s[0] in a1.accept and s[2]=='1':
                accept.add(s)

    a=Automaton(W,a1.alphabet|a2.alphabet,transitions,start,accept)

    a=find_and_change_cycles(a)
    optimize(a)

    return a
