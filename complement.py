import itertools
from automaton import *
from optimize import *
from atomic_automata import *
from intersection import input_equal

def one_start_state(b):
    """Automaton will have only one start state."""

    b.states.add("new")
    # add transitions from new start state
    old_transitions=copy(b.transitions)
    for t in old_transitions:
        if t[0] in b.start:
            b.transitions.append(("new",t[1],t[2]))
            if not any(i[0]==t[0] and i[0]==i[2] for i in old_transitions):
                # remove old start states without self loop
                b.transitions.remove(t)
            elif t[0]==t[2]:
                # old start state with self loop won't be removed
                b.transitions.append(("new",t[1],t[2]))
            # if one of the old start states was accepting, the new one will be as well
            if t[0] in b.accept:
                b.accept.add("new")

    # remove old start states
    for s in copy(b.start):
        if not any(t[0] in b.states or t[2] in b.states for t in b.transitions):
            b.states.remove(s)
    
    b.start={"new"}

    # remove accept states
    for s in copy(b.accept):
        if s not in b.states:
            b.accept.remove(s)

    b.transitions=list(b.transitions)
    for i in range(len(b.transitions)):
        b.transitions[i]=list(b.transitions[i])

    # remove duplicate transitions
    tran=list()
    for t in b.transitions:
        if t not in tran:
            tran.append(t)
    b.transitions = copy(tran)

    edit_names(b)
    edit_transitions(b)
    optimize(b)


def complement(a):
    """Constructs complement of a Buchi automaton a."""

    if a==true():
        return false()
    elif a==false():
        return true()

    # level ranking is a function g: a.states -> {0,...,2*|a.states|}U{-1}
    # -1 indicates that the state is not present in the level of the run DAG
    maxRanking = 2*len(a.states)
    
    # level ranking
    all_combinations=list(itertools.product(set(range(maxRanking+1))|{-1}, repeat=len(a.states)))
    R=list()    # list of all level rankings
    for i in range(len(all_combinations)):
        dictionary={}
        j=0
        skip=False
        for state in a.states:
            # assign some value from {0,...,2*|a.states|}U{-1} to each state
            # accept state can't be ranked with an odd number
            if state in a.accept and all_combinations[i][j]!=-1 and all_combinations[i][j]%2==1:
                skip=True
                break
            dictionary[state]=all_combinations[i][j]
            j+=1
        if not skip:
            R.append(dictionary)
    
    # start states
    start=list()
    accept=list()
    not_start=set(a.states)-set(a.start)  # all states that are not start states
    for dictionary in R:
        # state is ranked with '_' iff it is not a start state
        if (all (dictionary[state]!=-1 for state in a.start)) and (all (dictionary[state]==-1 for state in not_start)):
            # first component identifies the level ranking
            # second component tracks the states whose corresponding vertices in the run DAG have even ranks
            start.append((dictionary, set()))
            accept.append((dictionary, set()))
    
    # transitions
    states = copy(start)
    transitions=list()
    for state in states:
        for c in a.alphabet:
            reachable_states = set()
            for t in a.transitions:
                if t[0] in state[0] and state[0][t[0]]!=-1 and input_equal(c, t[1]):
                    # reachable states
                    reachable_states.add(t[2])
            
            # find level ranking that covers state[0]
            # ranking has to be lower or equal for every state
            not_reachable=a.states-reachable_states
            for dictionary in R:
                if all((dictionary[q]<=max(state[0].values()) and dictionary[q]!=-1) for q in reachable_states) and all(dictionary[q]==-1 for q in not_reachable):
                    # second component of a state
                    P=set()
                    for q in a.states:
                        if dictionary[q]%2==0:
                            if state[1]!=set():
                                if q in state[1]:
                                    P.add(q)
                            else:
                                P.add(q)
                    new=(dictionary, P)
                    transitions.append([state, c, new])
                    if new not in states:
                        states.append(new)
                    if P==set() and new not in accept:
                        accept.append(new)

    b=Automaton(states, a.alphabet, transitions, start, accept)
    edit_names(b)
    optimize(b)
    
    one_start_state(b)  # automaton will have only one start state

    return b
