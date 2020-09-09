"""Optimizations for Buchi automata."""

from automaton import *
from intersection import *

def remove_states_with_no_arrows_out(a):
    """Removes states from which it can"t be reached to any other state (including the state itself)."""

    end=False
    while not end:
        end=True
        for s in a.states:
            if all(s!=t[0] for t in a.transitions):
                end=False
                for i in a.transitions:
                    if tuple(i[2])==s:
                        a.transitions.remove(i)
                a.states.remove(s)
    return a


def tarjan(a):
    """Tarjan's algorithm."""
    
    index=0
    stack=[]    # empty stack
    visited={i : [-1,-1,False] for i in a.states} # state : [index,lowlink,onStack]
    all_components=list()

    def scc(v):
        """Inner functions to find strongly connected components"""

        nonlocal index

        # Set the depth index for v to the smallest unused index
        visited[v][0]=index
        visited[v][1]=index
        index+=1
        stack.append(v)
        visited[v][2]=True

        # Successors of v
        for w in a.states:
            if any(tuple(t[2])==w and t[0]==v for t in a.transitions):
                if visited[w][0]==-1:
                    # Successor w has not yet been visited -> recurse
                    scc(w)
                    visited[v][1]=min(visited[v][1],visited[w][1])
                elif visited[w][2]:
                    # Successor w is on stack and hence in the current SCC
                    # If w is not on stack, then (v,w) is a transition pointing to an SCC already found and must be ignored
                    visited[v][1]=min(visited[v][1],visited[w][0])
        
        # If v is a root state, pop the stack and generate a SCC
        if visited[v][1]==visited[v][0]:
            # Start a new strongly connected component
            component=set()
            w=stack.pop()
            while w!=v:
                visited[w][2]=False
                # Add w to current scc
                component.add(w)
                w=stack.pop()
            visited[w][2]=False
            component.add(w)
            all_components.append(component)

    for v in visited:
        if visited[v][0] == -1:
            scc(v)

    return all_components

def remove_useless_scc(a):
    """Removes useless strongly connected components - components from which we can't reach to any other scc and no state in scc is accepting or components containing only one accepting state with no transition from it."""

    components=tarjan(a)
    #remove=True
    for c in components:
        remove=True
        if (not any(state in a.accept for state in c)) or (len(c)==1 and all(state in a.accept for state in c)):
            for state in c:
                if any((t[0]==state and tuple(t[2]) not in c) for t in a.transitions):
                    remove=False
                if len(c)==1 and state in a.accept and any((t[0]==state and tuple(t[2])==state) for t in a.transitions):
                    remove=False
            if remove:
                for state in c:
                    a.states.remove(state)
                    if state in a.start:
                        a.start.remove(state)
                    if state in a.accept:
                        a.accept.remove(state)
                    transitions=copy(a.transitions)
                    for t in transitions:
                        if t[0]==state or tuple(t[2])==state:
                            a.transitions.remove(t)

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
    """Removes unreachable parts of an automaton."""

    # Find all reachable states
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
    
    # Remove useless transitions
    transitions2=copy(a.transitions)
    for t in a.transitions:
        if t[0] not in reachable or tuple(t[2]) not in reachable:
            transitions2.remove(t)
    a.transitions=copy(transitions2)
    
    # Remove unreachable states
    states=copy(a.states)
    for s in states:
        if s not in reachable:
            a.states.remove(s)
    
    # Remove unreachable accept states
    accept2=copy(a.accept)
    for i in a.accept:
        if not any(t[0]==i or tuple(t[2])==i for t in a.transitions):
            accept2.remove(i)
    a.accept=copy(accept2)
    
    return a
