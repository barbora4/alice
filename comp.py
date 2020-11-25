import itertools
from automaton import *
from optimize import *
from atomic_automata import *
from intersection import input_equal
from complement import *

def comp(a):
    """Constructs complement of a Buchi automaton a."""

    if a==true():
        return false()
    elif a==false():
        return true()

    # level ranking is a function g: a.states -> {0,...,2*|a.states|}U{-1}
    # -1 indicates that the state is not present in the level of the run DAG
    maxRanking = 2*len(a.states-a.accept)
    
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
    start=[copy(a.start)]
    accept=list()

    Q1=[copy(a.states)]
    Q2=list()

    # transitions
    states = copy(start)
    transitions=list()
    i=0
    while i < len(states):
        for c in a.alphabet:
            reachable_states = set()
                     
            if states[i] not in Q2 and all(q in a.states for q in states[i]): 
                # reachable states
                for t in a.transitions:
                    if t[0] in states[i] and input_equal(c, t[1]):
                        reachable_states.add(t[2])
                
                # first type of transitions
                P=set()
                for t in a.transitions:
                    if t[2] in reachable_states and input_equal(c, t[1]) and t[0] in states[i]:
                        P.add(t[2])     # all states reachable from reachable_states with input c
                if P not in states:
                    states.append(P)
                transitions.append([states[i], c, P])
                if len(P)==0 and P not in accept:
                    accept.append(P)
        
        
                # second type of transitions
                not_reachable=a.states-reachable_states
                for ranking in R:
                    # ranking is S-tight for S==reachable_states
                    if all(ranking[q]==-1 for q in not_reachable) and all(ranking[q]%2==1 and ranking[q]!=-1 for q in reachable_states):
                        new = [P, set(), ranking, 0]
                        if new not in Q2:
                            states.append(new)
                            Q2.append(new)
                            if len(new[1])==0:
                                accept.append(new)
                        transitions.append([states[i], c, new])

        
            elif states[i] in Q2:
                # third type of transitions
                # reachable states
                reachable_states=set()
                for t in a.transitions:
                    if t[0] in states[i][0] and input_equal(c,t[1]):
                        reachable_states.add(t[2])
                not_reachable=a.states-reachable_states

                # level ranking has to be lower or equal
                for ranking in R:
                    skip=False
                    if all(ranking[q]==-1 for q in not_reachable):
                        for q in reachable_states:
                            maximum = -1
                            for t in a.transitions:
                                if t[2]==q and t[0] in states[i][0] and input_equal(c, t[1]):
                                    maximum = max(maximum, states[i][2][t[0]])
                            if not (ranking[q]<=maximum and ranking[q]!=-1):
                                skip=True
                                break
                            
                        if not skip:
                            # same ranking
                            if max(ranking.values())==max(states[i][2].values()):
                                # first option
                                if len(states[i][1])==0:
                                    if max(ranking.values())==-1:   #???
                                        j=states[i][3]
                                    else:
                                        j=(states[i][3]+2)%(max(ranking.values())+1) ### modulo by (-1+1)=0???
                                    O=set()
                                    for q in a.states:
                                        if ranking[q]==j:
                                            O.add(q)
                                    new_state=[reachable_states, O, ranking ,j]
                                    if new_state not in states:
                                        states.append(new_state)
                                        Q2.append(new_state)
                                    transitions.append([states[i], c, new_state])

                                # second option
                                else:
                                    j=states[i][3]
                                    O=set()
                                    O1=set()
                                    O2=set()
                                    for t in a.transitions:
                                        if t[0] in states[i][1] and input_equal(c,t[1]):
                                            O1.add(t[2])
                                    for q in a.states:
                                        if ranking[q]==j:
                                            O2.add(q)
                                    O=O1&O2 # intersection
                                    new_state=[reachable_states, O, ranking, j]
                                    if new_state not in states:
                                        states.append(new_state)
                                        Q2.append(new_state)
                                    transitions.append([states[i], c, new_state])

        i+=1

    b=Automaton(states, a.alphabet, transitions, start, accept)
    optimize(b)
    one_start_state(b)  # automaton will have only one start state

    return b
