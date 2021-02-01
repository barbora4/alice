###################################################################
# Barbora Šmahlíková
# 2020/2021
# NBA complementation
###################################################################

import itertools
from automaton import *
from optimize import *
from atomic_automata import *
from intersection import input_equal

def comp2(a):
    """Constructs complement of a Buchi automaton a."""

    if a==true():
        return false()
    elif a==false():
        return true()

    # level ranking is a function g: a.states -> {0,...,2*|a.states|}
    # 1 indicates that the state is not present in the level of the run DAG
    maxRanking = 2*(len(a.states)-len(a.accept))

    all_combinations = list()
    for state in a.states:
        if state in a.accept:
            all_combinations.append(list(range(maxRanking+1))[::2]) #!!!   
        else:
            all_combinations.append(list(range(maxRanking+1)))
    all_combinations = list(product(*all_combinations))
    R=list()
    for i in range(len(all_combinations)):
        dictionary={}
        j=0
        for state in a.states:
            dictionary[state]=all_combinations[i][j]
            j+=1
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
                     
            if states[i] not in Q2 and (all(q in a.states for q in states[i])): 
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
                if [states[i], c, P] not in transitions:
                    transitions.append([states[i], c, P])
                if len(P)==0 and P not in accept:
                    accept.append(P)
        

                # second type of transitions
                not_reachable = a.states - P
                for rank in R:
                    ranking = copy(rank)
                    skip=False
                    # ranking is S-tight for S==reachable_states
                    for q in not_reachable: 
                        ranking[q]=1
                    if max(ranking.values())%2==1:
                        # at least one state in S is mapped to every odd number up to max(ranking.values())
                        for j in range(1,max(ranking.values())+1,2): # odd numbers up to max(ranking.values())
                            if sum(x==j for x in ranking.values())==0:
                                # no state mapped onto this number
                                skip=True
                                break
                        if not any(ranking[q] == 1 for q in P):
                            skip=True
                        
                        if not skip:
                            new = [P, set(), ranking, 0]
                            if new not in Q2:
                                states.append(new)
                                Q2.append(new)
                                accept.append(new)
                            if [states[i], c, new] not in transitions:
                                transitions.append([states[i], c, new])

        
            elif states[i] in Q2:
                # third type of transitions
                # reachable states
                reachable_states=set()
                for t in a.transitions:
                    if t[0] in states[i][0] and input_equal(c,t[1]):
                        reachable_states.add(t[2])
                not_reachable=a.states-reachable_states

                P=set()
                for t in a.transitions:
                    if t[2] in reachable_states and input_equal(c, t[1]) and t[0] in states[i][0]:
                        P.add(t[2])     # all states reachable from reachable_states with input c

                not_reachable = a.states-P 
            
                # level ranking has to be lower or equal
                max_function_state = list()
                new_state=list()
                for rank in R:
                    #max_function_state=list()
                    #new_state=list()

                    ranking = copy(rank)
                    skip=False
                    
                    for q in not_reachable:
                        ranking[q]=1

                    # S-tight
                    if max(ranking.values())%2==1: # odd rank
                        for j in range(1, max(ranking.values())+1, 2): 
                            if sum(x==j for x in ranking.values())==0:
                                skip=True
                                break
                            if j==1: #!!!!!
                                if not any(ranking[q]==1 for q in P):
                                    skip=True
                    else:
                        skip=True

                    if not skip:
                        for q in P:    
                            minimum = maxRanking
                            for t in a.transitions:
                                if t[2]==q and t[0] in states[i][0] and input_equal(c, t[1]):
                                    minimum = min(minimum, states[i][2][t[0]])
                            if not (ranking[q]<=minimum):
                                skip=True
                                break 

                    if not skip:
                        # same ranking
                        if max(ranking.values())==max(states[i][2].values()):
                            # first option
                            if len(states[i][1])==0:
                                j=(states[i][3]+2)%(max(ranking.values())+1) 
                                O=set()
                                for q in a.states:
                                    if ranking[q]==j:
                                        O.add(q)
                                
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

                            new_state = [P, O, ranking, j]

                            if new_state not in states:
                                states.append(new_state)
                                Q2.append(new_state)
                                if len(O)==0:
                                    accept.append(new_state)
                            if [states[i], c, new_state] not in transitions:
                                transitions.append([states[i], c, new_state])

        i+=1

    b=Automaton(states, a.alphabet, transitions, start, accept)
    optimize(b)
    one_start_state(b)  # automaton will have only one start state

    return b
