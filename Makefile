s1s: automaton.py intersection.py optimize.py main.py union.py basic_automata.py
	python3 main.py
	dot -Tps graph.gv -o graph.pdf
