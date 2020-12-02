s1s: automaton.py intersection.py optimize.py main.py union.py atomic_automata.py parser.py complement.py direct.py comp.py comp2.py tree.py
	python3 main.py
	cat a.ba
	dot -Tpng graph.gv -o graph.png
	xdg-open graph.png &
	dot -Tpng tree.gv -o tree.png
	xdg-open tree.png &
