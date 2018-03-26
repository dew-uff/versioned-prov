::SET BASE = generated/mutable_prov::
::SET NAME = Mutable-PROV::

# ::GET NAME::

In this document we map simple script constructs to ::GET NAME::.

**This extension were discontinued in favor of [Versioned-PROV](versioned-prov.html)**


## Extension

Our extension adds the following components:

| Components                            | Description |
|:------------------------------------- |:------------------------------------------------------------ |
| value(`vid`, [repr="`t`"])            | Value `vid` with initial representation `t`.                 |
| defined(`e`, `v`, `t`)                | The entity `e` defined the value `v` at the time `t`.        |
| wasDefinedBy(`v`, `e`, `t`)           | The value `v` was defined by the entity `e` at the time `t`. |
| accesed(`e`, `v`, `t`)                | The entity `e` accessed the value `v` at the time `t`.       |
| accessedPart(`e`, `w`, `k`, `p`, `t`) | The entity `e` accessed the part value `p` at the key `k` <br> of the collection value `w` at the time `t`.    |
| derivedByInsertion(<br>&nbsp;&nbsp;&nbsp;&nbsp;`e`, `w`, {(`k`<sub>`1`</sub>, `p`<sub>`1`</sub>), ..., (`k`<sub>`n`</sub>, `p`<sub>`n`</sub>)}, `t`)               | The entity `e` derived the collection value `w` by the insertion<br> of the part values `p`<sub>`i`</sub> at the corresponding key `k`<sub>`i`</sub> <br>for `i` ∈ `1..n` at the time `t`. |
| derivedByRemoval(<br>&nbsp;&nbsp;&nbsp;&nbsp;`e`, `w`, {`k`<sub>`1`</sub>, ..., `k`<sub>`n`</sub>}, `t`) | The entity `e` derived the collection value `w` was derived by<br> the removal of the keys `k`<sub>`i`</sub> for `i` ∈ `1..n` at the time `t`. |

## Names, literals, and constants

During the script execution, function calls, literals (e.g., "a", 1, True), names, and all expressions that may produce any value are evaluations. In our mapping, we represent evaluations as `entities`.

In addition to the `entities`, we use the `defined` relationship to associate them to their evaluated values and the `wasDefinedBy` relationship to associate the evaluated values to the `entities` that defined them.

In our `values` we are using the attribute `repr` to indicate their representation during the creation. However, since `values` are mutable structures, this `repr` attribute may not correspond to the actual values.


```python
1     # literal
"a"   # literal
b"a"  # literal
True  # literal
int   # names
...   # constant
```

::PROV[::GET NAME:: mapping for names, literals, and constants](::GET BASE::/names)


## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the value used by each entity in a given time.

If the element on the left side of the assignment has the same value as the element on the right, we use the `accessed` relationship instead of the `defined`.

```python
m = 10000
```

::PROV[::GET NAME:: mapping for assignments](::GET BASE::/assign)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `defined` relationship to associate it to a `value`. Otherwise, we use the `accessed` relationship.

```python
m + 1
```

::PROV[::GET NAME:: mapping for operations](::GET BASE::/operation)


## List definition

A list is defined and represented by the `derivedByInsertion` relationship.

```python
[m, m + 1, m]
```

::PROV[::GET NAME:: mapping for list definitions](::GET BASE::/list)


Comparison:

* ::GET NAME:: accesses to parts indicates the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall. Note however that we do not navigate from the list entity `list1` to the part entity `m1` in a derivation query. Instead, we navigate to the entity that defined the value of `m1`. We could have a similar structure to the other approaches with an activity using `m1` and `sum1` and generating `list1` without a derivation relationship to indicate this usage. Since this usage does not affect the provenance query of Floyd-Warshall, we opted to leave it out.


## Assignment of list definition

With ::GET NAME::, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `accessed` relationship to indicate that accessed value by the entity.

```python
d = [m, m + 1, m]
```

::PROV[::GET NAME:: mapping for assignments of list definitions](::GET BASE::/list_assign)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

::PROV[::GET NAME:: mapping for assignments to names that have list definitions](::GET BASE::/list_assign2)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return.

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

::PROV[::GET NAME:: mapping for function call](::GET BASE::/call)


## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the `accessedPart` relationship to indicate which part were accessed.

```python
d[0]
```

::PROV[::GET NAME:: mapping for accesses to parts](::GET BASE::/access)


## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the `derivedByInsertion` to update the collection value withe the new part value.


```python
d[1] = 3
```

::PROV[::GET NAME:: mapping for assignments to parts](::GET BASE::/part_assign)

Comparison:

* With ::GET NAME::, we just need to update the `value`. All entities that `accessed` the value keep the same

## Full graph

The full mapping for the previous code is presented below:

```python
>>> m = 10000
>>> d = [m, m + 1, m]
>>> x = d
>>> len(d)
3
>>> d[0]
10000
>>> d[1] = 3
```

::PROV[::GET NAME:: mapping](::GET BASE::/full)

# Floyd-Warshall

This mapping produced the following graph for Floyd-Warshall:

::![Floyd-Warshall in ::GET NAME::](::GET BASE::/floydwarshall)

# Query

The ::GET NAME:: mapping produces the following query result:

::![Query in ::GET NAME::](::GET BASE::/query)
