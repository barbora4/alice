from automaton import *
from itertools import product

def direct_simulation(a):
    """Direct simulation for automaton a."""

    # cardinality
    card={}
    for c in a.alphabet:
        dic={}
        for q in a.states:
            dic[q]=0
            for t in a.transitions:
                if t[0]==q and input_equal(c,t[1]):
                    dic[q] += 1
        card[c]=dic

    # matrices - initialize all N(a)s with 0s
    mat = {}
    for c in a.alphabet:
        N = list()
        for i in range(len(a.states)):
            N.append([0]*len(a.states))
        mat[c] = N

    w = set()   # the relation which is the complement of direct simulation at the end
    queue = []
    
    for i in a.accept:
        for j in (a.states-a.accept):
            w.add((i, j))
            queue.append((i, j))

    while len(queue)!=0:
        new = queue.pop(0)    # dequeue
        for c in a.alphabet:
            for t in a.transitions:
                if t[2] == new[1] and input_equal(c, t[1]):
                    mat[c][int(new[0])][int(t[0])] += 1
                    if mat[c][int(new[0])][int(t[0])] == card[c][t[0]]:
                        for t2 in a.transitions:
                            if t2[2]==new[0] and input_equal(c, t2[1]): #####
                                if (t2[0], t[0]) not in w: #####
                                    w.add((t2[0], t[0])) #####
                                    queue.append((t2[0],t[0])) #####
    
    all_combinations = set(product(a.states, a.states))
    direct = all_combinations - w   # direct simulation

    return direct


def reduction(a):

    edit_names(a)
    edit_transitions(a)

    change = True
    while change:
        change = False
        direct = direct_simulation(a)

        for d in direct:
            if (d[1],d[0]) in direct and d[0]!=d[1]:
                # merge these two states and update preorder
                change = True
                # add new state
                a.states.add("new")
                if d[0] in a.start or d[1] in a.start:
                    a.start.add("new")
                if d[0] in a.accept or d[1] in a.accept:
                    a.accept.add("new")
                # remove old states
                a.states.remove(d[0])
                if d[1] in a.states:
                    a.states.remove(d[1])
                if d[0] in a.start:
                    a.start.remove(d[0])
                if d[1] in a.start:
                    a.start.remove(d[1])
                if d[0] in a.accept:
                    a.accept.remove(d[0])
                if d[1] in a.accept:
                    a.accept.remove(d[1])
                # adjust transitions
                for i in range(len(a.transitions)):
                    if a.transitions[i][0]==d[0] or a.transitions[i][0]==d[1]:
                        a.transitions[i][0]="new"
                    if a.transitions[i][2]==d[0] or a.transitions[i][2]==d[1]:
                        a.transitions[i][2]="new"
                # remove duplicate transitions
                tran = list()
                for t in a.transitions:
                    if t not in tran:
                        tran.append(t)
                a.transitions = copy(tran)
                # edit names and transitions
                edit_names(a)
                edit_transitions(a)
                break
