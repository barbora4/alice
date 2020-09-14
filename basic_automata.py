"""Construction of basic Buchi automata."""

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
    alphabet=alphabet_x|alphabet_Y

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
    alphabet=alphabet_x|alphabet_y

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

    for a in alphabet2:
        if a not in alphabet1:
            # add to alphabet
            alphabet1.add(a)
            a1.alphabet.add("{}:0".format(a))
            a1.alphabet.add("{}:1".format(a))
            # add to all transitions
            for i in range(len(a1.transitions)):
                a1.transitions[i]=list(a1.transitions[i])
                a1.transitions[i][1]="{}|{}".format(a1.transitions[i][1],"{}:{}".format(a,'?'))
                a1.transitions[i]=tuple(a1.transitions[i])

def add_all_variables(a1,a2):
    """Adds variables that are only in one automaton to the second one."""

    alphabet1=get_all_variables(a1)
    alphabet2=get_all_variables(a2)

    add_to_transitions(a1,alphabet1,alphabet2)
    add_to_transitions(a2,alphabet2,alphabet1)

