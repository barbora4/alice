s1s: automaton.py intersection.py optimize.py main.py union.py atomic_automata.py parser.py complement.py direct.py comp.py comp2.py
	python3 main.py
	dot -Tpdf graph.gv -o graph.pdf
	evince graph.pdf &
	cat a.ba
