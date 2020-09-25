"""LISP parser."""

from automaton import Automaton
from intersection import *
from union import *
from basic_automata import *

def parse(f):
    """Creates a list of elements from LISP formula."""

    with open(f) as f:
        text=f.read()

    formula=[]
    element=""
    left=0  # number of parentheses
    right=0
    for c in text:
        # parentheses
        if c=='(' or c==')':
            if element!="":
                formula.append(element)
                element=""
            formula.append(c)
            if c=='(':
                left+=1
            if c==')':
                right+=1
        # skip spaces
        elif c.isspace() and element!="":
            formula.append(element)
            element=""
        # load whole element
        elif not c.isspace():
            element+=c

    if left!=right:
        raise SyntaxError("Invalid form of formula.")
    
    return create_automaton(formula)    


def create_automaton(formula):
    """Creates Buchi automaton from LISP formula in file f."""
    
    stack=[]
    atom=[]
    for element in formula:
        if element!=")":
            stack.append(element)
        else:
            atom.append(element)
            # pop everything to '(' and add to atom
            while(stack[-1]!="("):
                atom.append(stack.pop())
            atom.append(stack.pop())
            atom.reverse()

            # operations with automata
            if atom[1]=="exists":
                a=exists(atom[2],atom[3])
            elif atom[1]=="and":
                a=intersection(atom[2],atom[3])
            elif atom[1]=="or":
                a=union(atom[2],atom[3])

            # atomic automata
            elif atom[1]=="zeroin":
                a=zeroin(atom[2])
            elif atom[1]=="sub":
                print(atom)
                a=sub(atom[2],atom[3])
            elif atom[1]=="succ":
                a=succ(atom[2],atom[3])
            else:
                # arguments of succ or sub are in parentheses
                atom.remove('(')
                atom.remove(')')
                atom.reverse()
                for i in range(len(atom)):
                    stack.append(atom[len(atom)-i-1])
                atom=[]
                continue

            stack.append(a)
            atom=[]

    return a
