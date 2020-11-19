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

Formula:
```
(and (neg (zeroin X)) (neg (succ (X Y))))
```
Image:

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph2.png" width=400>

| | |
| --- | --- |
| Direct simulation | -3 states |
| Disconnecting little brothers | no change |

---

Formula:
```
(or
  (implies
    (neg
      (or
        (neg (and (sing X) (zeroin X)))
        (succ (X Y))
    ))
    (sub (X Y))
  )
  (and (succ (X Y)) (zeroin Y))
)
```
Image:

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph3.png" width=400>

| | |
| --- | --- |
| Direct simulation | -3 states |
| Disconnecting little brothers | no change |

---

Formula:
```
(exists U
  (neg
    (implies 
      (forall V (implies (succ (V U)) (sub (V Z))))
      (sub (U Z))
)))
```
Image:

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph1_02.png" width=400>

| | |
| --- | --- |
| Direct simulation | -11 states |
| Disconnecting little brothers | -11 transitions |

---

Formula:
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
Image:

<img src="https://github.com/barbora4/projektova-praxe/blob/master/images/graph4.png" width=400>

| | |
| --- | --- |
| Direct simulation | -8 states |
| Disconnecting little brothers | -3 transitions |
