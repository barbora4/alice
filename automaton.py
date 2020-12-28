"""Class Automaton, loading data from .ba files and writing to them."""

import re
import csv
from copy import copy
from dataclasses import dataclass

@dataclass
class Automaton:
    """Data class representing an automaton."""

    states: set
    alphabet: set
    transitions: list
    start: set
    accept: set

def load_data(file):
    """Loads data from .ba file to object Automaton."""

    start=set()         # start states
    transitions=list()  # transitions: [input, start, end]  
    accept=set()        # accept states
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
                transitions.append([match.group(3), match.group(1), match.group(5)]) 
                alphabet.add(match.group(1))
                states.add(match.group(3))
                states.add(match.group(5))
        
            # accept states
            elif re.search(r"^\[(.)+\]\n$", line) and not beginning:
                accept.add(line[1:-2])
                states.add(line[1:-2])
            
            # wrong file format
            else:
                raise SyntaxError("Wrong format!")

    return Automaton(states,alphabet,transitions,start,accept)


def write_all_transitions(a):
    while any('?' in tran[1] for tran in a.transitions):
        transitions = list()
        for t in a.transitions:
            if '?' not in t[1]:
                transitions.append(t)
            else:
                transitions.append([t[0], t[1].replace('?', '0', 1), t[2]])
                transitions.append([t[0], t[1].replace('?', '1', 1), t[2]])
        a.transitions = copy(transitions)

def write_to_file(a,f):
    """Writes automaton to .ba file."""

    with open(f, "w") as f:
        # start states
        for i in a.start:
            if type(i)==tuple:
                f.write('[{}]\n'.format(','.join(map(str,i))))
            else:
                f.write('[{}]\n'.format(i))
        
        # transitions
        for i in a.transitions:
            if type(i[0])==tuple:
                t1='[%s]'%','.join(map(str, i[0]))
            else:
                t1="[{}]".format(i[0])
            if type(i[2])==tuple:
                t2='[%s]'%','.join(map(str, i[2]))
            else:
                t2="[{}]".format(i[2])
            f.write("{},{}->{}\n".format(i[1],t1,t2))
        
        # accept states
        for i in a.accept:
            if type(i)==tuple:
                f.write('[{}]\n'.format(','.join(map(str,i))))
            else:
                f.write('[{}]\n'.format(i))


def write_to_gv(a,f):
    """Writes automaton a into .gv file f."""

    with open(f, "w") as f:
        # beginning
        f.write("digraph buchi_automaton {\n")
        f.write("\trankdir=LR;\n")
        f.write('\tsize="8,5"\n')
        f.write("\tnode [shape = doublecircle];")
        for acc in a.accept:
            f.write(' "{}"'.format(acc))
        if len(a.accept)!=0:
            f.write(";\n")
        else:
            f.write("\n")
        if len(a.states)!=0:
            f.write('\tinit [label="", shape=point]\n')
        f.write("\tnode [shape = circle];\n")

        # transitions
        for s in a.start:
            f.write('\tinit -> "{}"\n'.format(s))
        for t in a.transitions:
            f.write('\t"{}" -> "{}" [ label = "{}" ]\n'.format(t[0], t[2], t[1]))

        # end
        f.write("}\n")


def edit_names(a):
    """Renames all states with numbers, starting with 0."""

    dictionary={}
    i=0
    for state in a.states:
        dictionary[str(i)]=state
        i+=1

    # rename states
    a.states=list(a.states)
    for i in range(len(a.states)):
        a.states[i]=list(dictionary.keys())[list(dictionary.values()).index(a.states[i])]
    a.states=set(a.states)

    # rename start states
    a.start=list(a.start)
    for i in range(len(a.start)):
        a.start[i]=list(dictionary.keys())[list(dictionary.values()).index(a.start[i])]
    a.start=set(a.start)

    # rename accept states
    a.accept=list(a.accept)
    for i in range(len(a.accept)):
        a.accept[i]=list(dictionary.keys())[list(dictionary.values()).index(a.accept[i])]
    a.accept=set(a.accept)

    # rename transitions
    for i in range(len(a.transitions)):
        a.transitions[i][0]=list(dictionary.keys())[list(dictionary.values()).index(a.transitions[i][0])]
        a.transitions[i][2]=list(dictionary.keys())[list(dictionary.values()).index(a.transitions[i][2])]


def edit_transitions(a):
    """Edits transitions -> substitutes 0/1 with '?' wherever possible."""

    transitions2=copy(a.transitions)
    edit=True

    while edit:
        edit=False
        for t1 in range(len(a.transitions)):
            for t2 in range(len(a.transitions)):
                # two transitions with the same start and accept states
                if a.transitions[t1][0]==a.transitions[t2][0] and a.transitions[t1][2]==a.transitions[t2][2] and a.transitions[t1][1]!=a.transitions[t2][1]:
                    count=0     # how many characters are different
                    change=""   # new transition name
                    for c1,c2 in zip(a.transitions[t1][1],a.transitions[t2][1]):
                        if c1!=c2:
                            count+=1
                            change+="?"
                        else:
                            change+=c1
                    
                    # only one different character -> substitute with '?'
                    if count==1:
                        edit=True
                        new=[a.transitions[t1][0],change,a.transitions[t1][2]]
                        if a.transitions[t1] in transitions2:
                            transitions2.remove(a.transitions[t1])
                        if a.transitions[t2] in transitions2:
                            transitions2.remove(a.transitions[t2])
                        if new not in transitions2:
                            transitions2.append(new)

        a.transitions=copy(transitions2)

def input_equal(a,t):
    """Returns True if inputs a and t are equal."""
    
    if '|' not in a:
        if a==t:
            return True

    # divide into variables
    a_list=list()
    a_list=list(a.split('|'))
    a_list.sort()

    t_list=list()
    t_list=list(t.split('|'))
    t_list.sort()

    # substitute ? with 0 or 1
    for i in range(len(a_list)):
        if not (a_list[i]==t_list[i] or a_list[i].replace('?','0')==t_list[i] or a_list[i].replace('?','1')==t_list[i] or t_list[i].replace('?','0')==a_list[i] or t_list[i].replace('?','1')==a_list[i]):
            return False
    
    return True

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


def complete_automaton(a):
    complete = True
    for q in a.states:
        for c in a.alphabet:
            if not any(t[0]==q and input_equal(c, t[1]) for t in a.transitions):
                complete = False
                break
    
    if not complete:
        a.states.add("new")
        for q in a.states:
            for c in a.alphabet:
                if not any(t[0]==q and input_equal(c, t[1]) for t in a.transitions):
                    a.transitions.append([q, c, "new"])

    edit_names(a)
