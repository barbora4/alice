"""Intersection of two Buchi automata"""

import itertools
from copy import copy
from automaton import Automaton
from basic_automata import cylindrification

def input_equal(a,t):
    """Returns True if inputs a and t are equal."""

    if '|' not in a:
        if a==t:
            return True

    # divide into variables
    a_list=list()
    a_list=list(a.split('|'))
    a_list.sort()

    t_list=list()
    t_list=list(t.split('|'))
    t_list.sort()

    # substitute ? with 0 or 1
    for i in range(len(a_list)):
        if not (a_list[i]==t_list[i] or a_list[i].replace('?','0')==t_list[i] or a_list[i].replace('?','1')==t_list[i] or t_list[i].replace('?','0')==a_list[i] or t_list[i].replace('?','1')==a_list[i]):
            return False
    
    return True

def edit_names(states):
    """Removes tuples from name of a state."""

    states=list(states)
    for i in range(len(states)):
        for j in range(len(states[i])):
            if type(states[i][j])==tuple:
                states[i]=list(states[i])
                states[i][j]="{}".format(','.join(map(str,states[i][j])))
                states[i]=tuple(states[i])
    return set(states)


def intersection(a1,a2):
    """Algorithm for intersection of 2 Buchi automata."""

    # add all variables to input alphabet and transitions
    cylindrification(a1,a2)

    # edit names
    a1.states=edit_names(a1.states)
    a1.start=edit_names(a1.start)
    a1.accept=edit_names(a1.accept)
    a2.states=edit_names(a2.states)
    a2.start=edit_names(a2.start)
    a2.accept=edit_names(a2.accept)

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

    # edit names
    W=edit_names(W)
    start=edit_names(start)
    accept=edit_names(accept)
    for index in {0,2}:
        for i in range(len(transitions)):
            for j in range(len(transitions[i][index])):
                if type(transitions[i][index][j])==tuple:
                    transitions[i][index]=list(transitions[i][index])
                    transitions[i][index][j]="{}".format(','.join(map(str,transitions[i][index][j])))
                    transitions[i][index]=tuple(transitions[i][index])

    return Automaton(W,a1.alphabet|a2.alphabet,transitions,start,accept)

