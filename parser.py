"""LISP parser."""

from automaton import Automaton
from intersection import *
from union import *
from atomic_automata import *
from comp2 import *
from tree import *

def analyse_predicates(file_text):
    """Analyses user-defined predicates."""

    predicates={}

    # user-defined predicates
    lines = file_text.split('\n')
    error=False
    for line in lines:
        if len(line)!=0 and line.split()[0]=="#define": #line[0]=='#':
            my_predicate=""
            i=7
            if not line[i].isspace():
                error=True
                break
            
            # skip spaces
            while i<len(line) and line[i].isspace():
                i+=1

            if line[i]!='(':
                # wrong format
                error=True
                break

            # predicate in parentheses
            left=0
            right=0
            while i<len(line):
                if line[i]=='(':
                    left+=1
                elif line[i]==')':
                    right+=1
                my_predicate+=line[i]
                i+=1
                if left==right and left!=0:
                    break

            while i<len(line) and line[i].isspace():
                i+=1
            if i==len(line):
                error=True
            
            # predicate definition
            definition=""
            while i<len(line):
                definition+=line[i]
                i+=1
            
            new_pred=""
            i=1
            while i<len(my_predicate):
                if my_predicate[i]=='(' or my_predicate[i].isspace():
                    break
                new_pred+=my_predicate[i]
                i+=1
            
            variables=[]
            while i<len(my_predicate):
                if my_predicate[i].isalpha():
                    variables.append(my_predicate[i])
                i+=1

            predicates[new_pred]=[variables, definition]
        
        else:
            break

    if error:
        raise SyntaxError("Wrong format of user-defined predicates!")

    return predicates


def parse(file_text, predicates):
    """Creates a list of elements from LISP formula."""

    # skip lines with user-defined predicates
    lines = file_text.split('\n')
    new_text=""
    for line in lines:
        if not(len(line)!=0 and line[0]=='#'):
            new_text+=line

    formula=[]
    element=""
    left=0  # number of parentheses
    right=0
    for c in new_text:
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
    

    create_tree(formula, predicates)
    #return create_automaton(formula, predicates)   
    
    
def create_automaton(formula, predicates):
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
            error=False

            # user-defined predicates
            if atom[1] in predicates.keys():
                tmp=predicates[atom[1]][1]  # predicate definition
                i=2
                for var in predicates[atom[1]][0]:
                    tmp = tmp.replace(var, atom[i]) # replace formal arguments with actual arguments
                    i+=1
                a=parse(tmp, predicates) # create automaton for predicate

            # operations with automata
            elif atom[1]=="exists":
                if not (isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a=exists(atom[2],atom[3])
            elif atom[1]=="forall":
                if not (isinstance(atom[3], Automaton)):
                    error=True
                else:
                    #a=complement(exists(atom[2], complement(atom[3])))
                    a=comp2(exists(atom[2], comp2(atom[3])))
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
                    #a=complement(atom[2])
                    #a=comp(atom[2])
                    a=comp2(atom[2])
            elif atom[1]=="implies":
                if not (isinstance(atom[2], Automaton) and isinstance(atom[3], Automaton)):
                    error=True
                else:
                    #a=union(complement(atom[2]), atom[3])
                    a=union(comp2(atom[2]), atom[3])

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
