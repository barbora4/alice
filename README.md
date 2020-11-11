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
