from automaton import *
from intersection import *
from union import *
from optimize import *

# load data from file
with open(input("Enter a file with the first automaton: ")) as f1:
    a1=load_data(f1)
with open(input("Enter a file with the second automaton: ")) as f2:
    a2=load_data(f2)

# intersection
a=intersection(a1,a2)
optimize(a)
write_to_file(a,"intersection.ba")

# union
a=union(a1,a2)
write_to_file(a,"union.ba")
