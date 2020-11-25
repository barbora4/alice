# Input syntax for S1S formulae

## Built-in constructions

|			|				|
| ---			| ---				|
| (exists X (...))	| Existential quantifier	|
| (forall X (...))	| Universal quantifier		|
| (neg (...))		| Negation			|
| (and (...) (...))	| Conjunction			|
| (or (...) (...))	| Disjunction			|
| (implies (...) (...))	| Implication			|
| (sub (X Y))		| X <span>&#8838;</span> Y	|
| (succ (X Y))		| X is a successor of Y		|
| (zeroin X)		| 0 <span>&#8712;</span> X	|
| (sing X)		| X is a singleton		|

## User-defined predicates

Use syntax similar to syntax for macros in C

```c
#define (my_predicate (list_of_arguments)) (...)
```

### Example

```c
#define (not_sub (X Y)) (neg (sub (X Y)))

(not_sub (Y Z))
```

## Statistics

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/formula1">Formula:</a>
```
(exists U
  (neg
    (implies 
      (forall V (implies (succ (V U)) (sub (V Z))))
      (sub (U Z))
)))
```

| Formula | Remove useless SCC | Direct simulation | Little brothers |
| --- | --- | --- | --- |
| A: (implies (succ (V U)) (sub (V Z))) | -1 state | -1 state | - |
| B: (forall V A) | -5 states | -4 states | -8 transitions |
| C: (implies B (sub (U Z))) | -1 state | -2 states | - |
| D: (neg C) | -2 states | - | - |
| E: (exists U D) | -1 state | - | - |
| Total | -10 states | -7 states | -8 transitions |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph1_02.png" width=400>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/formula2">Formula:</a>
```
(or
  (exists U
    (and
      (neg
        (exists V
          (and (succ (V U)) (neg (sub (V Z))))
        )
      )
      (neg
        (sub (U Z))
      )
    )
  )
  (neg (sub (Y Z)))
)
```

| Formula | Remove useless SCC | Direct simulation | Little brothers |
| --- | --- | --- | --- |
| A: (neg (sub (V Z))) | - | -1 state | - |
| B: (and (succ (V U)) A) | - | -1 state | - |
| C: (exists V B) | - | -1 state | - |
| D: (neg C) | -1 state | - | - |
| E: (neg (sub (U Z))) | - | -1 state | - |
| F: (and D E) | - | -1 state | - |
| G: (exists U F) | - | - | - |
| H: (neg (sub (Y Z))) | - | -1 state | - |
| I: (or G H) | -1 state | - | - |
| Total | -2 states | -6 states | - |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph5.png" width=400>


