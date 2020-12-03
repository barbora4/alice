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

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f01">Formula:</a>
```
(and
  (sing X)
  (or
    (and (sub X Z) (neg (sub X Y)))
    (and (sub X Y) (neg (sub X Z)))
  )
)
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (neg (sub X Y)) | 4 | - | -1 state | - | 3 |
| B: (and (sub X Z) A) | 3 | - | -1 state | - | 2 |
| C: (neg (sub X Z)) | 4 | - | -1 state | - | 3 |
| D: (and (sub X Y) C) | 3 | - | -1 state | - | 2 |
| E: (or B D) | 5 | - | - | - | 5 |
| F: (and (sing X) E) | 11 | -4 states | -2 states | - | 5 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f01.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f01_tree.png" width=300></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f02">Formula:</a>
```
(neg (exists X
  (and
    (sing X)
    (or
      (and (sub X Z) (neg (sub X Y)))
      (and (sub X Y) (neg (sub X Z)))
    )
  )
))
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (neg (sub X Y)) | 4 | - | -1 state | - | 3 |
| B: (and (sub X Z) A) | 3 | - | -1 state | - | 2 |
| C: (neg (sub X Z)) | 4 | - | -1 state | - | 3 |
| D: (and (sub X Y) C) | 3 | - | -1 state | - | 2 |
| E: (or B D) | 5 | - | - | - | 5 |
| F: (and (sing X) E) | 11 | -4 states | -2 states | - | 5 |
| G: (exists X F) | 5 | - | - | - | 5 |
| H: (neg G) | 13 | -9 states | -1 state | - | 3 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f02.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f02_tree.png" width=300></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f22">Formula:</a>
```
(implies
  (and (sing J) (sub J U))
  (or
    (and (sing I) (sub I V))
    (and (sing I) (sub I W))
  )
)
```

| Formula | States before reduction | Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (sing I) (sub I V)) | 2 | - | - | - | 2 |
| B: (and (sing I) (sub I W)) | 2 | - | - | - | 2 |
| C: (or A B) | 5 | - | -1 state | - | 4 |
| D: (and (sing I) (sub J U)) | 2 | - | - | - | 2 |
| E: (implies D C) | 10 | -2 states | - | - | 8 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f22.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f22_tree.png" width=300></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f06">Formula:</a>
```
(and
  (and (sing X) (sing Y))
  (succ Y X)
)
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (sing X) (sing Y)) | 6 | - | - | - | 6 |
| B: (and A (succ X Y)) | 4 | - | - | - | 4 |


<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f06.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f06_tree.png" width=300></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f07">Formula:</a>
```
#define (suc X Y) (and (and (sing X) (sing Y)) (succ X Y))

(exists Z
  (and
    (suc X Z) (suc Z Y))
  )
)
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (suc Z X) (suc Y Z)) | 5 | - | - | - | 5 |
| B: (exists Z A) | 5 | - | - | - | 5 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f07.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f07_tree.png" width=300></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f08">Formula:</a>
```
#define (suc2 X Y) (exists A (and (and (sing X) (and (sing Y) (sing A))) (and (succ X A) (succ A Y))))

(exists Z
  (and
    (suc2 X Z) (suc2 Z Y))
  )
)
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (suc2 X Z) (suc2 Z Y)) | 15 | - | -5 states | - | 10 |
| B: (exists Z A) | 10 | - | - | - | 10 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f08.png" width=500></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f08_tree.png" width=500></img>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f09">Formula:</a>
```
#define (suc4 X Y) (exists B (and (exists A (and (and (sing X) (and (sing B) (sing A))) (and (succ X A) (succ A B)))) (exists A (and (and (sing B) (and (sing Y) (sing A))) (and (succ B A) (succ A Y))))))

(exists Z
  (and (suc4 X Z) (suc4 Z Y))
)
```

| Formula | States before reduction |Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (suc4 X Z) (suc4 Z Y)) | 28 | - | -10 states | - | 18 |
| B: (exists Z A) | 18 | - | - | - | 18 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f09.png" width=800>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f09_tree.png" width=800>

---

<a href="https://github.com/barbora4/projektova-praxe/blob/master/benchmark/f16">Formula:</a>
```
(exists U
  (and
    (and (sing U) (sub U X))
    (neg
      (exists V (< V U))
    )
  )
)
```

| Formula | States before reduction | Remove useless SCC | Direct simulation | Little brothers | States after reduction |
| --- | --- | --- | --- | --- | --- |
| A: (and (sing U) (sub U X)) | 2 | - | - | - | 2 |
| B: (exists V (< V U)) | 3 | - | - | - | 3 |
| C: (neg B) | 14 | -8 states | -1 state | - | 5 |
| D: (and A C) | 16 | -12 states | -1 state | - | 3 |
| E: (exists U D) | 3 | - | - | - | 3 |

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f16.png" width=400></img>
<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/f16_tree.png" width=300></img>

---

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

