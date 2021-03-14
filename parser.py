###################################################################
# Barbora Šmahlíková
# 2020/2021
# S1S formula parser
###################################################################

from automaton import Automaton
from intersection import *
from union import *
from atomic_automata import *
from complement import *
from tree import *
import math
import itertools
import re
from copy import deepcopy

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

            a = parse(definition, predicates)
            tmp = 1
            for var in variables:
                for i in range(len(a.transitions)):
                    a.transitions[i][1] = a.transitions[i][1].replace(var, "#"+str(tmp))
                new_alphabet = set()
                for symbol in a.alphabet:
                    new = symbol.replace(var, "#"+str(tmp))
                    new_alphabet.add(new)
                a.alphabet = deepcopy(new_alphabet)
                tmp += 1

            if "--rabit" in sys.argv:
                a = rabit_reduction(a)
            
            predicates[new_pred]=[len(variables), a]
        
        else:
            break

    if error:
        raise SyntaxError("Wrong format of user-defined predicates!")

    return predicates


def parse(file_text, predicates):
    """Creates a list of elements from S1S formula."""

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
    

    #create_tree(formula, predicates)
    a = create_automaton(formula, predicates) 
    edit_transitions(a)
    return a 
    
    
def create_automaton(formula, predicates):
    """Creates Buchi automaton from S1S formula."""
    
    if "--spot" in sys.argv:
        spot = True
    else:
        spot = False
    if "--rabit" in sys.argv:
        rabit = True
    else:
        rabit = False
    
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
                a = deepcopy(predicates[atom[1]][1])
                for i in range(predicates[atom[1]][0]):
                    for j in range(len(a.transitions)):
                        a.transitions[j][1] = a.transitions[j][1].replace("#"+str(i+1), atom[i+2])
                    new_alphabet = set()
                    for symbol in a.alphabet:
                        new = symbol.replace("#"+str(i+1), atom[i+2])
                        new_alphabet.add(new)
                    a.alphabet = deepcopy(new_alphabet)

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
                    a = atom[3]
                    if spot:
                        a = spot_complement(a)
                    else:
                        a=comp2(a)
                    a = exists(atom[2], a)
                    if rabit:
                        a = rabit_reduction(a)
                    if spot:
                        a = spot_complement(a)
                    else:
                        a=comp2(a)
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
                    a = atom[2]
                    if spot:
                        a = spot_complement(a)
                    else:
                        a=comp2(a)
            elif atom[1]=="implies":
                if not (isinstance(atom[2], Automaton) and isinstance(atom[3], Automaton)):
                    error=True
                else:
                    a = atom[2]
                    if spot:
                        a = spot_complement(a)
                    else:
                        a = comp2(a)
                    if rabit:
                        a = rabit_reduction(a)
                    a=union(a, atom[3])

            # atomic automata
            elif atom[1]=="zeroin":
                a=zeroin(atom[2])
            elif atom[1]=="sing":
                a=sing(atom[2])
            elif atom[1]=="sub":
                a=sub(atom[2],atom[3])
            elif atom[1]=="succ":
                a=succ(atom[2],atom[3])
            elif atom[1]=="<":
                a=less(atom[2],atom[3])
            
            else:
                if (not first) or len(atom)!=4:
                    raise SyntaxError('Invalid form of input formula near "{}".'.format(' '.join(map(str,atom))))
                if isinstance(atom[2], Automaton) or isinstance(atom[3], Automaton):
                    raise SyntaxError('Invalid form of input formula near "{}".'.format(atom[1]))

                # arguments of succ or sub can be in parentheses
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

            # reduction
            if rabit:
                a = rabit_reduction(a)

    return a

def rabit_reduction(a):
    "Using Rabit for reduction"

    alphabet = a.alphabet
    write_all_transitions(a)
    write_to_file(a, 'a.ba') # write to a.ba
    stream = os.popen('java -jar ../RABIT250/Reduce.jar a.ba 10')
    output = stream.read()
    #print(output)
    with open('reduced_10_a.ba') as f:
        a = load_data(f) # reduced automaton
    a.alphabet = alphabet
    
    return a


def myfunc():
    if not hasattr(myfunc, "counter"):
        myfunc.counter = 0
    myfunc.counter += 1
    return myfunc.counter

def spot_complement(a):
    "Using Spot for complement"
    
    a = rabit_reduction(a)

    alphabet = a.alphabet
    complete_automaton(a)
    
    # write to .ba file
    write_all_transitions(a)
    write_to_file(a, 'a.ba')
    stream = os.popen('cat a.ba')
    output = stream.read()
    
    # convert to .hoa
    with open('a.hoa', 'w+') as f:
        f.write('HOA: v1\n')
        f.write('States: {}\n'.format(len(a.states)))
        f.write('Start:')
        for state in a.start:
            f.write(" {}".format(state))
        f.write('\n')
        f.write('acc-name: Buchi\n')
        f.write('Acceptance: 1 Inf(0)\n')
        f.write('properties: explicit-labels state-acc trans-labels\n')
        f.write('AP: {}'.format(int(math.log(len(a.alphabet),2))))
        for c in a.alphabet:
            i=0
            symbol_count = 0
            symbols=list()
            while i<len(c):
                f.write(' "{}"'.format(c[i]))
                symbol_count += 1
                symbols.append(c[i])
                i+=4
            break
        f.write('\n')
        f.write('--BODY--\n')
        for state in a.states:
            f.write('State: {}'.format(state))
            if state in a.accept:
                f.write(' {0}')
            f.write('\n')
            for t in a.transitions:
                if t[0]==state:
                    string=""
                    i=0
                    while i<symbol_count:
                        if "{}:0".format(symbols[i]) in t[1]:
                            word = "!{}".format(i)
                        else:
                            word = "{}".format(i)
                        if i==0:
                            string += word
                        else:
                            string += " & {}".format(word)
                        i+=1
                    f.write('[{}] {}\n'.format(string, t[2]))
        f.write('--END--\n')

    # export .hoa files
    #endFile = 'aut/'+sys.argv[-1]+'-'+str(myfunc())+'.hoa'
    #stream = subprocess.Popen('cp a.hoa ' + endFile, shell=True)
    #stream.wait()

    # complement using spot
    stream = subprocess.Popen('autfilt --complement --ba a.hoa >a_neg.hoa', shell=True)
    stream.wait()

    b = Automaton(set(), a.alphabet, list(), set(), set())
    with open('a_neg.hoa') as src:
        for line in src:
            if "States" in line:
                split = line.split()
                for state in split:
                    if state.isdigit():
                        for i in range(int(state)):
                            b.states.add(str(i))
            elif "Start" in line:
                split = line.split()
                for state in split:
                    if state.isdigit():
                        b.start.add(state)
            elif "State:" in line:
                split = line.split()
                for s in split:
                    if s.isdigit():
                        current = s
                    elif "{0}" in s:
                        b.accept.add(current)
            elif "[" in line:
                split = line.split()
                for state in split:
                    if state.isdigit():
                        dst = state
                
                newline = re.search('\[(.+?)\]',line).group(1)
                newline = newline.replace('[','')
                newline = newline.replace(']','')
                newline = newline.replace('|','')
                split = newline.split()
                for option in split:
                    string=""
                    for i in range(symbol_count):
                        if "!{}".format(i) in option:
                            if i==0:
                                string += "{}:0".format(symbols[i])
                            else:
                                string += "|{}:0".format(symbols[i])
                        elif str(i) in option:
                            if i==0:
                                string += "{}:1".format(symbols[i])
                            else:
                                string += "|{}:1".format(symbols[i])
                        else:
                            if i==0:
                                string += "{}:?".format(symbols[i])
                            else:
                                string += "|{}:?".format(symbols[i])
                    if [current, string, dst] not in b.transitions:
                        b.transitions.append([current, string, dst])
        
        write_all_transitions(b)
        write_to_file(b, 'a.ba')

    with open('a.ba') as f:
        a = load_data(f)
    a.alphabet = alphabet

    a = rabit_reduction(a)

    return a