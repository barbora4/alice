from automaton import *
from intersection import *
from optimize import *

with open(input("Enter a file with the first automaton: ")) as f1:
    a1=load_data(f1)
with open(input("Enter a file with the second automaton: ")) as f2:
    a2=load_data(f2)

# construction
a=intersection(a1,a2)
a=remove_states_with_no_arrows_out(a)

# 3rd optimization: looking for cycles
a=find_and_change_cycles(a)

# remove unreachable parts
a=remove_unreachable_parts(a)

tarjan(a)

# writing to file
with open("intersection.ba", "w") as f:
    for i in a.start:
        f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))
    for i in a.transitions:
        f.write("{},[{},{},{}]->[{},{},{}]\n".format(i[1],i[0][0],i[0][1],i[0][2],i[2][0],i[2][1],i[2][2]))
    for i in a.accept:
        f.write("[{},{},{}]\n".format(i[0],i[1],i[2]))
