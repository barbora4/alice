from automaton import *
from itertools import product

def direct_simulation(a):
    """Direct simulation for automaton a."""

    # remove duplicate transitions
    tran=list()
    for t in a.transitions:
        if t not in tran:
            tran.append(t)
    a.transitions = copy(tran)

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

    # states with cardinality 0
    # card[c][y]==0 and card[c][x]!=0 => w.add((x,y))
    for c in a.alphabet:
        for x in a.states:
            for y in a.states:
                if card[c][y]==0 and card[c][x]!=0:
                    w.add((x,y))

    while len(queue)!=0:
        new = queue.pop(0)    # dequeue
        for c in a.alphabet:
            for t in a.transitions:
                if t[2] == new[1] and input_equal(c, t[1]): # all k for which new[1]c->k
                    mat[c][int(new[0])][int(t[0])] += 1
                    if mat[c][int(new[0])][int(t[0])] == card[c][t[0]]: # there is j: new[0]c->j for which (j,k) in w for all states k 
                        for t2 in a.transitions:
                            if t2[2]==new[0] and input_equal(c, t2[1]): 
                                if (t2[0], t[0]) not in w:
                                    w.add((t2[0], t[0])) 
                                    queue.append((t2[0],t[0])) 
    
    all_combinations = set(product(a.states, a.states))
    direct = all_combinations - w   # direct simulation
    return direct

def merge(a, q0, q1):
    """Merges two states in automaton a."""

    # merge these two states and update preorder
    # add new state
    a.states.add("new")
    if q0 in a.start or q1 in a.start:
        a.start.add("new")
    if q0 in a.accept or q1 in a.accept:
        a.accept.add("new")
    # remove old states
    a.states.remove(q0)
    if q1 in a.states:
        a.states.remove(q1)
    if q0 in a.start:
        a.start.remove(q0)
    if q1 in a.start:
        a.start.remove(q1)
    if q0 in a.accept:
        a.accept.remove(q0)
    if q1 in a.accept:
        a.accept.remove(q1)
    # adjust transitions
    for i in range(len(a.transitions)):
        if a.transitions[i][0]==q0 or a.transitions[i][0]==q1:
            a.transitions[i][0]="new"
        if a.transitions[i][2]==q0 or a.transitions[i][2]==q1:
            a.transitions[i][2]="new"
    # remove duplicate transitions
    tran = list()
    for t in a.transitions:
        if t not in tran:
            tran.append(t)
    a.transitions = copy(tran)
    

def reduction(a):
    """Reduces states in automaton a using direct simulation."""

    change = True
    while change:
        edit_names(a)
        edit_transitions(a)

        change = False
        skip=False
        direct = direct_simulation(a)

        for d in direct:
            if (d[1],d[0]) in direct and d[0]!=d[1]:
                change=True
                merge(a, d[0], d[1])
                skip=True
                break
        
        if not skip:
            # reversed automaton
            b=Automaton(copy(a.states), copy(a.alphabet), list(), copy(a.accept), copy(a.start))
            for t in a.transitions:
                b.transitions.append([t[2], t[1], t[0]])
            
            left = direct_simulation(b)
            for d in left:
                if (d[1],d[0]) in left and d[0]!=d[1]:
                    change=True
                    merge(a, d[0], d[1])
                    skip=True
                    print("ahoj")
                    break

            if not skip:
                for d in direct:
                    if d in left and d[0]!=d[1]:
                        change=True
                        merge(a, d[0], d[1])
                        break
                
