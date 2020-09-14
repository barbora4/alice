"""Construction of basic Buchi automata."""

from copy import copy
from itertools import product
from automaton import Automaton

def zero_in_X(X):
    """Constructs Buchi automaton for formula: 0 is an element of X."""

    start={"0"}
    accept={"1"}
    alphabet=["{}:0".format(X), "{}:1".format(X)]
    # first input must be X:1
    for s in start:
        for a in accept:
            transitions=[[s,alphabet[1],a], [a,alphabet[0],a], [a,alphabet[1],a]]
    states=start|accept

    return Automaton(states,set(alphabet),transitions,start,accept)


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
        a.transitions[i]=tuple(a.transitions[i])

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


def add_all_variables(a1,a2):
    """Adds variables that are only in one automaton to the second one and sorts input variables alphabetically."""

    alphabet1=get_all_variables(a1)
    alphabet2=get_all_variables(a2)

    add_to_transitions(a1,alphabet1,alphabet2)
    add_to_transitions(a2,alphabet2,alphabet1)

    alphabetical_order(a1)
    alphabetical_order(a2)
