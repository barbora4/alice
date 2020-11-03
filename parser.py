"""LISP parser."""

from automaton import Automaton
from intersection import *
from union import *
from atomic_automata import *
from complement import *

def parse(f):
    """Creates a list of elements from LISP formula."""

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
        raise SyntaxError("Invalid form of input formula (parentheses not matching).")
    
    return create_automaton(formula)    


def create_automaton(formula):
    """Creates Buchi automaton from LISP formula in file f."""
    
    stack=[]
    atom=[]
    first=True  
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
            error=False
            if atom[1]=="exists":
                if not (isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=exists(atom[2],atom[3])
            elif atom[1]=="forall":
                if not (isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=complement(exists(atom[2], complement(atom[3])))
            elif atom[1]=="and":
                if not (isinstance(atom[2], Automaton) and isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=intersection(atom[2],atom[3])
            elif atom[1]=="or":
                if not (isinstance(atom[2], Automaton) and isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=union(atom[2],atom[3])
            elif atom[1]=="neg":
                if not (isinstance(atom[2], Automaton)):
                    error=True
                else:
                    a=complement(atom[2])
            elif atom[1]=="implies":
                if not (isinstance(atom[2], Automaton) and isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=union(complement(atom[2]), atom[3])

            # atomic automata
            elif atom[1]=="zeroin":
                a=zeroin(atom[2])
            elif atom[1]=="sing":
                a=sing(atom[2])
            elif atom[1]=="sub":
                a=sub(atom[2],atom[3])
            elif atom[1]=="succ":
                a=succ(atom[2],atom[3])
            else:
                if (not first) or len(atom)!=4:
                    raise SyntaxError('Invalid form of input formula near "{}".'.format(' '.join(map(str,atom))))
                if isinstance(atom[2], Automaton) or isinstance(atom[3], Automaton):
                    raise SyntaxError('Invalid form of input formula near "{}".'.format(atom[1]))

                # arguments of succ or sub are in parentheses
                atom.remove('(')
                atom.remove(')')
                atom.reverse()
                for i in range(len(atom)):
                    stack.append(atom[len(atom)-i-1])
                atom=[]
                first=False
                continue

            if error:
                raise SyntaxError('Invalid form of input formula near "{}".'.format(atom[1]))
            stack.append(a)
            first=True
            atom=[]

    return a
