###################################################################
# Barbora Šmahlíková
# 2020/2021
# Writing automaton to .gv file
###################################################################

from complement import *
from optimize import *
from parser import *

def write_to_gv(a,f):
    """Writes automaton a into .gv file f."""

    with open(f, "w") as f:
        # beginning
        f.write("digraph buchi_automaton {\n")

        # language emptiness test -> decide satisfiability of a formula
        if len(a.states)==1 and len(a.transitions)==0:
            f.write('\tlabel = "Empty language,\nunsatisfiable formula";\n')
            print("Empty language, unsatisfiable formula")
        else:
            f.write('\tlabel = "Satisfiable formula";\n')
            print("Satisfiable formula")

        # testing validity of a formula
        if "--validity" in sys.argv:
            if "--spot" in sys.argv:
                b = spot_complement(a)
            else:
                b = comp2(a)
            if "--rabit" in sys.argv:
                b = rabit_reduction(b)
            empty = optimize(b)
            if empty:
                f.write('\tlabel= "Valid formula"\n;')
                print("Valid formula")
            else:
                f.write('\tlabel= "Invalid formula"\n;')
                print("Invalid formula")

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
