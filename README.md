# Translation of S1S formula to Büchi automaton

## Input syntax for S1S formulae

### Atomic formulae

|	Formula |	Input format |
| ---			| ---				|
| 0 <span>&isin;</span> X | (zeroin X) |
| X <span>&sube;</span> Y | (sub X Y) |
| Sing(X) | (sing X) |
| Y = Succ(X) | (succ Y X) |
| X < Y| (< X Y) |

### Operations over automata
(A and B denotes formulae)

| Formula | Input format |
| --- | --- |
| <span>&not;</span>A | (neg A) |
| A<span>&and;</span>B | (and A B) |
| A<span>&or;</span>B | (or A B) |
| A<span>&rarr;</span>B | (implies A B) |
| <span>&exist;</span>X.A | (exists X A) |
| <span>&forall;</span>X.A | (forall X A) |


## User-defined predicates

Use syntax similar to syntax for macros in C

```c
#define (my_predicate list_of_arguments) (...)
```

### Example

```c
#define (not_sub X Y) (neg (sub X Y))

(and (not_sub U V) (zeroin V))
```

## Usage
```
python3 main.py [--rabit] [--spot] [--validity]
```

Use ```--rabit``` for reduction with a simulation using lookahead 10 

Requirements: Install <a href="http://languageinclusion.org/doku.php?id=tools">Rabit</a> into a parent directory (```../RABIT250/Reduce.jar```)

Use ```--spot``` for complementation using external tool

Requirements: Install <a href="https://spot.lrde.epita.fr/autfilt.html">Spot</a>

Use ```--validity``` to determine validity of the input formula

### Output

The final automaton is saved in ```a.ba``` and the graph is in ```graph.pdf```

### Experiments

Formulae used for experiments are in ```benchmark/```

### Example
<b>Formula</b>: <span>(x&isin;Y&and;x&notin;Z) &or; (x&isin;Z&and;x&notin;Y)</span>

<b>Input syntax</b>:
```
(or
 (and 
  (and (sub X Z) (neg (sub X Y))) 
  (sing X)
 )
 (and 
  (sub X Y) 
  (and (neg (sub X Z)) (sing X))
 )
)
```

<b>a.ba</b>: <br/>
[0] <br/>
X:1|Y:0|Z:1,[0]->[1] <br/>
X:1|Y:1|Z:0,[0]->[1] <br/>
X:0|Y:?|Z:?,[1]->[1] <br/>
X:0|Y:?|Z:?,[0]->[0] <br/>
[1] <br/>

<b>graph.pdf</b>: <br/>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f01.png"></img>
