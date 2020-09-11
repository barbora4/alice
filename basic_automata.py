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

    return Automaton(states,alphabet,transitions,start,accept)
