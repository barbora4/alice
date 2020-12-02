import itertools
from automaton import *
from optimize import *
from atomic_automata import *
from intersection import input_equal
from complement import *

def comp2(a):
    """Constructs complement of a Buchi automaton a."""

    if a==true():
        return false()
    elif a==false():
        return true()

    # level ranking is a function g: a.states -> {0,...,2*|a.states|}U{-1}
    # -1 indicates that the state is not present in the level of the run DAG
    maxRanking = 2*(len(a.states)-len(a.accept))
    
    all_combinations = list()
    for state in a.states:
        if state not in a.accept:
            all_combinations.append(list(range(maxRanking+1)))
        else:
            all_combinations.append(list(range(maxRanking+1))[::2])
    all_combinations = list(product(*all_combinations))
    print(len(all_combinations))
    R=list()
    for i in range(len(all_combinations)):
        dictionary={}
        j=0
        for state in a.states:
            dictionary[state]=all_combinations[i][j]
            j+=1
        R.append(dictionary)
    print(len(R))

    """
    # level ranking
    all_combinations=list(itertools.product(set(range(maxRanking+1))|{-1}, repeat=len(a.states)))
    print(len(all_combinations))
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
    """

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
        print(len(states))
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
                for rank in R:
                    ranking = copy(rank)
                    skip=False
                    # ranking is S-tight for S==reachable_states
                    #!!! if all(ranking[q]==-1 for q in not_reachable) and all(ranking[q]%2==1 and ranking[q]!=-1 for q in reachable_states):
                    if all(ranking[q]%2==1 for q in reachable_states): #!!!
                        for q in not_reachable: #!!!
                            ranking[q]=-1       #!!!
                        # ranking has to be maximal w.r.t. states[i]
                        # ranking maps all accepting states in the run to max(ranking.values())-1
                        if all(ranking[q]==max(ranking.values())-1 for q in a.accept&(states[i])):
                            # exactly one state is mapped to every odd number smaller than max(ranking.values())
                            for j in range(1,max(ranking.values()),2): # odd number smaller than max(ranking.values())
                                if sum(x==j for x in ranking.values())!=1:
                                    skip=True
                                    break
                            # all remaining states are mapped to max(ranking.values())
                            for q in a.states:
                                if ranking[q]%2!=1 or not(ranking[q]<max(ranking.values())):
                                    if ranking[q]!=max(ranking.values()):
                                        skip=True
                                        break
                        
                            if not skip:
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
                for rank in R:
                    ranking = copy(rank)
                    skip=False
                    #!!! if all(ranking[q]==-1 for q in not_reachable):
                    for q in not_reachable:
                        ranking[q]=-1#!!!
                    for q in reachable_states: ## shifted to the left!!!
                        maximum = -1
                        for t in a.transitions:
                            if t[2]==q and t[0] in states[i][0] and input_equal(c, t[1]):
                                maximum = max(maximum, states[i][2][t[0]])
                        if not (ranking[q]<=maximum): #!!! and ranking[q]!=-1):
                            skip=True
                            break
                        
                    if not skip:
                        end=False
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
                                
                            
                            # ranking has to be maximal w.r.t. states[i]
                            # ranking maps all accepting states in the run to max(ranking.values())-1
                            if all(ranking[q]==max(ranking.values())-1 for q in a.accept&(states[i][0])):
                                # exactly one state is mapped to every odd number smaller than max(ranking.values())
                                for j in range(1,max(ranking.values()),2): # odd number smaller than max(ranking.values())
                                    if sum(x==j for x in ranking.values())!=1:
                                        end=True
                                        break
                                # all remaining states are mapped to max(ranking.values())
                                for q in a.states:
                                    if ranking[q]%2!=1 or not(ranking[q]<max(ranking.values())):
                                        if ranking[q]!=max(ranking.values()):
                                            end=True
                                            break
                            
                                if not end:
                                    new_state=[reachable_states, O, ranking ,j]
                                    if new_state not in states:
                                        states.append(new_state)
                                        Q2.append(new_state)

                                    transitions.append([states[i], c, new_state])

                                    # fourth type of transitions
                                    if len(new_state[1])==0 or new_state[3]!=0:
                                        for r in R:
                                            if all(r[q]==new_state[2][q]-1 for q in new_state[1]):
                                                if all(r[q]==new_state[2][q] for q in a.states-new_state[1]):
                                                    other_state=[copy(new_state[0]), set(), r, copy(new_state[3])]
                                                    if other_state not in states:
                                                        states.append(other_state)
                                                        Q2.append(other_state)
                                                    transitions.append([states[i], c, other_state])

        i+=1

    b=Automaton(states, a.alphabet, transitions, start, accept)
    optimize(b)
    one_start_state(b)  # automaton will have only one start state

    return b
