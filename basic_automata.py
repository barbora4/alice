"""Construction of basic Buchi automata."""

from copy import copy
from itertools import product
from automaton import Automaton
from optimize import *

def x_in_Y(x,Y):
    """Constructs Buchi automaton for formula: x is in Y."""

    start={"0"}
    accept={"1"}
    states=start|accept

    alphabet_x={"{}:0".format(x), "{}:1".format(x)}
    alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
    alphabet=set()
    for a in alphabet_x:
        for b in alphabet_Y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    for s in start:
        for a in accept:
            # if index is not x, Y can be both 0 or 1 and we stay in the same state
            transitions.append([s,"{}:0|{}:0".format(x,Y),s])
            transitions.append([s,"{}:0|{}:1".format(x,Y),s])
            transitions.append([a,"{}:0|{}:0".format(x,Y),a])
            transitions.append([a,"{}:0|{}:1".format(x,Y),a])
            # if index is x, Y must be 1
            transitions.append([s,"{}:1|{}:1".format(x,Y),a])

    return Automaton(states,alphabet,transitions,start,accept)


def x_is_0(x):
    """Constructs Buchi automaton for formula: x is equal to 0."""

    start={"0"}
    accept={"1"}
    states=start|accept
    alphabet=["{}:0".format(x), "{}:1".format(x)]

    # index of x is 0
    for s in start:
        for a in accept:
            transitions=[[s,"{}:1".format(x),a], [a,"{}:0".format(x),a]]

    return Automaton(states,set(alphabet),transitions,start,accept)


def x_is_y(x,y):
    """Constructs Buchi automaton for formula: x is equal to y."""

    start={"0"}
    accept={"1"}
    states=start|accept
   
    alphabet_x={"{}:0".format(x), "{}:1".format(x)}
    alphabet_y={"{}:0".format(y), "{}:1".format(y)}
    alphabet=set()
    for a in alphabet_x:
        for b in alphabet_y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    for s in start:
        for a in accept:
            # index of x and y must be the same
            transitions.append([s,"{}:0|{}:0".format(x,y),s])
            transitions.append([a,"{}:0|{}:0".format(x,y),a])
            transitions.append([s,"{}:1|{}:1".format(x,y),a])

    return Automaton(states,alphabet,transitions,start,accept)


def get_all_variables(a):
    """Returns set of all used variables of automaton a."""
    
    alphabet=set()
    for i in a.alphabet:
        for j in set(i.split('|')):
            alphabet.add(j.split(':')[0])

    return alphabet

def add_to_transitions(a1,alphabet1,alphabet2):
    """Adds variables to transitions of a1."""

    old_alphabet=copy(a1.alphabet)
    change=False
    for a in alphabet2:
        if a not in alphabet1:
            change=True
            # add to alphabet
            alphabet1.add(a)
            for b in copy(a1.alphabet):
                a1.alphabet.add("{}|{}:0".format(b,a))
                a1.alphabet.add("{}|{}:1".format(b,a))
            # add to all transitions
            for i in range(len(a1.transitions)):
                a1.transitions[i][1]="{}|{}".format(a1.transitions[i][1],"{}:{}".format(a,'?'))

    if change:
        for a in old_alphabet:
            a1.alphabet.remove(a)

def alphabetical_order(a):
    """Sorts input variables in transitions alphabetically."""

    for i in range(len(a.transitions)):
        t=list(a.transitions[i][1].split('|'))
        t.sort()
        first=True
        for j in t:
            if first:
                a.transitions[i][1]=j
                first=False
            else:
                a.transitions[i][1]="{}|{}".format(a.transitions[i][1], j)

    new_alphabet=set()
    for i in a.alphabet:
        t=list(i.split('|'))
        t.sort()
        first=True
        for j in t:
            if first:
                i=j
                first=False
            else:
                i="{}|{}".format(i,j)
        new_alphabet.add(i)
    a.alphabet=copy(new_alphabet)


def cylindrification(a1,a2):
    """Adds variables that are only in one automaton to the second one and sorts input variables alphabetically."""

    alphabet1=get_all_variables(a1)
    alphabet2=get_all_variables(a2)

    add_to_transitions(a1,alphabet1,alphabet2)
    add_to_transitions(a2,alphabet2,alphabet1)

    alphabetical_order(a1)
    alphabetical_order(a2)


def exists(a,X):
    """Projection: eliminates X from the input alphabet and transitions of automaton a."""

    # remove X from the input alphabet
    alphabet=list(copy(a.alphabet))
    for i in range(len(alphabet)):
        t=list(alphabet[i].split('|'))
        for j in t:
            if X in j:
                t.remove(j)
        first=True
        for j in t:
            if first:
                alphabet[i]=j
                first=False
            else:
                alphabet[i]="{}|{}".format(alphabet[i],j)
    alphabet=set(alphabet)

    # remove X from all transitions
    transitions=copy(a.transitions)
    for i in transitions:
        t=list(i[1].split('|'))
        for j in t:
            if X in j:
                t.remove(j)
        first=True
        for j in t:
            if first:
                i[1]=j
                first=False
            else:
                i[1]="{}|{}".format(i[1],j)
        if first:
            i[1]=""

    # remove empty transitions
    for t in copy(transitions):
        if len(t[1])==0:
            transitions.remove(t)

    # remove duplicate transitions
    for t in transitions:
        if transitions.count(t)>1:
            transitions.remove(t)

    b=Automaton(a.states,alphabet,transitions,a.start,a.accept)
    remove_unreachable_parts(b)
    return b


def A_x(x):
    """Automaton to intersect with to make sure x appears exactly once."""

    a=x_is_0(x)
    for s in a.start:
        for acc in a.accept:
            a.transitions.append([s,"{}:0".format(x),s])

    return a


def exist_x(a,x):
    """Projection: eliminates x from the input alphabet and transitions of automaton a.

    Same as exist_X, but first is intersected with automaton that ensures that x appears only once (first-order variable)."""

    b=A_x(x)
    a=intersection(a,b)
    return exists(a,x)


def sub(X,Y):
    """Constructs atomic automaton for formula: X is a subset of Y."""

    start={"0"}
    accept=copy(start)
    states=start|accept
   
    alphabet_X={"{}:0".format(X), "{}:1".format(X)}
    alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
    alphabet=set()
    for a in alphabet_X:
        for b in alphabet_Y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    for s in start:
        # if an element is in X, it must be also in Y
        transitions.append([s,"{}:0|{}:?".format(X,Y),s])
        transitions.append([s,"{}:1|{}:1".format(X,Y),s])

    return Automaton(states,alphabet,transitions,start,accept)


def succ(Y,X):
    """Constructs atomic automaton for formula: Y is a successor of X."""

    start={"0"}
    accept=copy(start)|{"1"}
    states=start|accept
   
    alphabet_X={"{}:0".format(X), "{}:1".format(X)}
    alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
    alphabet=set()
    for a in alphabet_X:
        for b in alphabet_Y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    for s in start:
        for a in accept:
            if a not in start:
                transitions.append([s,"{}:0|{}:0".format(X,Y),s])
                transitions.append([s,"{}:1|{}:0".format(X,Y),a])
                transitions.append([a,"{}:1|{}:1".format(X,Y),a])
                transitions.append([a,"{}:0|{}:1".format(X,Y),s])
    
    return Automaton(states,alphabet,transitions,start,accept)


def zeroin(X):
    """Constructs Buchi automaton for formula: 0 is an element of X."""

    start={"0"}
    accept={"1"}
    alphabet=["{}:0".format(X), "{}:1".format(X)]
    
    transitions=list()
    # first input must be X:1
    for s in start:
        for a in accept:
                transitions.append([s,"{}:1".format(X),a])
                transitions.append([a,"{}:?".format(X),a])
    
    states=start|accept

    return Automaton(states,set(alphabet),transitions,start,accept)


