from automaton import *
from intersection import *
from optimize import *

with open(input("Enter a file with the first automaton: ")) as f1:
    a1=load_data(f1)
with open(input("Enter a file with the second automaton: ")) as f2:
    a2=load_data(f2)

# construction
a=intersection(a1,a2)

# looking for cycles
a=find_and_change_cycles(a)
# remove unreachable parts
a=remove_unreachable_parts(a)

# remove useless strongly connected components
remove_useless_scc(a)

# writing to file
write_to_file(a,"intersection.ba")

