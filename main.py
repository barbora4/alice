from automaton import *
from intersection import *
from union import *
from optimize import *
from basic_automata import *

# load data from file
with open(input("Enter a file with the first automaton: ")) as f1:
    a1=load_data(f1)
with open(input("Enter a file with the second automaton: ")) as f2:
    a2=load_data(f2)

# intersection
#a=intersection(a1,a2)
#optimize(a)
#write_to_file(a,"intersection.ba")

# union
#a=union(a1,a2)
#write_to_file(a,"union.ba")

# basic automata
a=zero_in_X('X')
write_to_file(a,"zero.ba")

a=x_in_Y('x','Y')
write_to_file(a,"xinY.ba")

a1=x_is_0('x')
write_to_file(a1,"xis0.ba")

a2=x_is_y('y','x')
write_to_file(a2,"xisy.ba")

add_all_variables(a1,a2)
a=union(a1,a2)
write_to_file(a,"1.ba")
a=intersection(a1,a2)
optimize(a)
write_to_file(a,"2.ba")
