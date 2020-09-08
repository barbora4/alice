import re
import itertools
from copy import copy
from dataclasses import dataclass

@dataclass
class Automaton:
    start: set
    transitions: set
    accept: set
    alphabet: set
    states: set

def load_data(file):
    start=set()         # set of start states
    transitions=set()   # set of transitions: [input, start, end]
    accept=set()        # set of accept states
    alphabet=set()      # set of all input symbols
    states=set()        # set of all states

    beginning=True      
    
    for line in file:
        # start states
        if re.search(r"^\[(.)+\]\n$", line) and beginning:
            start.add(line[1:-2])
            states.add(line[1:-2])

        else:
            match=re.search(r"^((.)+),\[((.)+)\]->\[((.)+)\]\n$", line)
            # transitions
            if match:
                beginning=False
                transitions.add((match.group(1), match.group(3), match.group(5)))
                alphabet.add(match.group(1))
                states.add(match.group(3))
                states.add(match.group(5))
        
            # accept states
            elif re.search(r"^\[(.)+\]\n$", line) and not beginning:
                accept.add(line[1:-2])
                states.add(line[1:-2])

            # wrong format
            else:
                raise FormatError("Wrong format!")

    a=Automaton(start,transitions,accept,alphabet,states)
    return a

# algorithm for intersection
def intersection(a1,a2,nfa):
    W=list(itertools.product(a1.start,a2.start, {1}))   
    start=set(copy(W))
    Q=set()   
    F=set()   
    transitions=list()   

    for q in W:
        Q.add(q)
        if q[0] in a1.accept and q[2]==1:
            F.add(q)
        for a in a1.alphabet|a2.alphabet:
            for t1 in a1.transitions:
                if t1[0]==a and t1[1]==q[0]:
                    for t2 in a2.transitions:
                        if t2[0]==a and t2[1]==q[1]:
                            if q[2]==1 and q[0] not in a1.accept:
                                transitions.append([q,a,[t1[2],t2[2],1]])
                                if (t1[2],t2[2],1) not in Q:
                                    W.append((t1[2],t2[2],1))
                            if q[2]==1 and q[0] in a1.accept:
                                if nfa:
                                    x=1
                                else:
                                    x=2
                                transitions.append([q,a,[t1[2],t2[2],x]])
                                if (t1[2],t2[2],x) not in Q:
                                    W.append((t1[2],t2[2],x))
                            if q[2]==2 and q[1] not in a2.accept:
                                transitions.append([q,a,[t1[2],t2[2],2]])
                                if (t1[2],t2[2],2) not in Q:
                                    W.append((t1[2], t2[2],2))
                            if q[2]==2 and q[1] in a2.accept:
                                transitions.append([q,a,[t1[2],t2[2],1]])
                                if (t1[2],t2[2],1) not in Q:
                                    W.append((t1[2],t2[2],1))
    accept=set()
    for s in W:
        if nfa:
            if s[0] in a1.accept and s[1] in a2.accept:
                accept.add(s)
        else:
            if s[0] in a1.accept and s[2]==1:
                accept.add(s)
    
    a=Automaton(start,transitions,accept,a1.alphabet|a2.alphabet,W)
    return a

def remove_unreachable_states(a):
    end=False
    while not end:
        for s in a.states:
            end=True
            if all(s!=t[0] for t in a.transitions):
                end=False
                for i in a.transitions:
                    if tuple(i[2])==s:
                        a.transitions.remove(i)
                a.states.remove(s)
    return a

def find_and_change_cycles(a):
    accept2=set()
    end=False
    while not end:
        end=True
        for q in a.accept:
            visited1=[[[q], list()]]
            for v in visited1:
                if (v[0][0]==q[0] and v[0][1]==q[1] and v[0][2]!=q[2]) or (q[0],q[1],2) not in a.states:
                    break
                seen_states=list()
                for t in a.transitions:
                    if t[0]==v[0][-1]:
                        seen_states=copy(v[0])
                        seen_states.append(tuple(t[2]))
                        new=copy([copy(seen_states), copy(v[1])]) 
                        if all(new[0][-1]!=u[0][-1] for u in visited1):
                            new[1].append(t[1])
                            visited1.append(new)
            visited2=list()
            for v in visited1:
                if v[0][-1][0]==q[0] and v[0][-1][1]==q[1] and v[0][-1][2]!=q[2]:#
                    visited2=[copy(v)]
                    new_state=[copy(v[0][-1])] 
                    new_state2=list()
                    new_list=copy(v[1])
                    for i in v[1]:
                        first=True
                        for t in a.transitions:
                            if t[0] in new_state and t[1]==i:
                                if first:
                                    new_list.remove(i)
                                    first=False
                                new=copy([copy(tuple(t[2])), copy(new_list)])
                                visited2.append(new) 
                                new_state2.append(tuple(t[2])) 
                                if len(new[1])==0 and new[0] in a.accept and new[0][0]==v[0][-1][0] and new[0][1]==v[0][-1][1]: 
                                    #print("\tNalezena smycka {} -> {} -> {}\n\tPro vstup {}".format(new[0],v[0][-1],new[0],2*v[1]))
                                    end=False
                                    accept2.add(v[0][-1])
                                    for t2 in a.transitions:
                                        if tuple(t2[2])[0]==v[0][0][0] and tuple(t2[2])[1]==v[0][0][1] and ((t2[0][0],t2[0][1],1) in v[0][:-1] or (t2[0][0],t2[0][1],2) in v[0][:-1]):
                                            t2[2][2]=(t2[2][2])%2+1
                        new_state=copy(new_state2)
    # add new accept states
    for q in accept2:
        a.accept.add(q)
    # remove old accept states
    accept2=copy(a.accept)
    for q in a.accept:
        if q not in a.states and q not in accept2:
            accept2.remove(q)
    a.accept=copy(accept2)
    return a

def remove_unreachable_parts(a):
    reachable=list()
    for st in a.start:
        reachable.append(st)
    quit=False
    while not quit:
        quit=True
        for t3 in a.transitions:
            if t3[0] in reachable and tuple(t3[2]) not in reachable:
                reachable.append(tuple(t3[2]))
                quit=False
    transitions2=copy(a.transitions)
    for t in a.transitions:
        if t[0] not in reachable or tuple(t[2]) not in reachable:
            transitions2.remove(t)
    a.transitions=copy(transitions2)
    return a


with open(input("Enter a file with the first automaton: ")) as f1:
    a1=load_data(f1)
with open(input("Enter a file with the second automaton: ")) as f2:
    a2=load_data(f2)


# 1st optimization: the construction for nfas can be used for nbas when all the states of one of the two nbas are accepting
nfa=all(q in a1.accept for q in a1.states) or all(q in a2.accept for q in a2.states)
# construction
a=intersection(a1,a2,nfa)

# remove duplicate transitions
for t in a.transitions:
    if a.transitions.count(t)>1:
        a.transitions.remove(t)

# 2nd optimization: remove states from which it can't be reached to any other state (including the state itself)
a=remove_unreachable_states(a)

# 3rd optimization: looking for cycles
a=find_and_change_cycles(a)

# remove unreachable parts
a=remove_unreachable_parts(a)

# remove unreachable accept states
accept2=copy(a.accept)
for i in a.accept:
    if not any(t[0]==i or tuple(t[2])==i for t in a.transitions):
        accept2.remove(i)
a.accept=copy(accept2)

# writing to file
with open("intersection.ba", "w") as f:
    for i in a.start:
        if nfa:
            f.write("[{},{}]\n".format(i[0],i[1]))
        else:
            f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))
    for i in a.transitions:
        if nfa:
            f.write("{},[{},{}]->[{},{}]\n".format(i[1],i[0][0],i[0][1],i[2][0],i[2][1]))
        else:
            f.write("{},[{},{},{}]->[{},{},{}]\n".format(i[1],i[0][0],i[0][1],i[0][2],i[2][0],i[2][1],i[2][2]))
    for i in a.accept:
        if nfa:
            f.write("[{},{}]\n".format(i[0],i[1]))
        else:
            f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))

