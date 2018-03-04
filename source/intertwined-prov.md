::SET BASE = images/intertwined_prov::
::SET NAME = Intertwined-PROV::

# ::GET NAME::

In this document we map simple script constructs to ::GET NAME::.

## Names, literals, and constants

During the script execution, function calls, literals (e.g., "a", 1, True), names, and all expressions that may produce any value are evaluations. In our mapping, we represent evaluations as `entities`.

All evaluation entities have versions. We represent versions by an entity with type `Version` and generatedAtTime indicating the time.

We associate evaluation entities to their versions by the relationship `specializationOf`.


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

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value as the element on the right, we use the `referenceDerivedFrom` relationship instead of the `wasDerivedFrom`.

This relationship indicates the time of derivation and allows us to get the version of the new entity by navigating from the left side entity to the right side entity.

```python
m = 10000
```

::PROV[::GET NAME:: mapping for assignments](::GET BASE::/assign)

## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we create a new version for it, and associate the entity to the version through the `specializationOf` relationship. Otherwise, we use the `referenceDerivedFrom` relationship.

```python
m + 1
```

::PROV[::GET NAME:: mapping for operations](::GET BASE::/operation)


## List definition

A list is defined and represented by a series of hadDictionaryMember on the version, indicating which entities are the parts.

```python
[m, m + 1, m]
```

::PROV[::GET NAME:: mapping for list definitions](::GET BASE::/list)


Comparison:

* In this mapping, accesses to parts indicate the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall.


## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `referenceDerivedFrom` relationship to indicate that the entity share a reference.

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

We also use the `referenceDerivedFromAccess` relationship to indicate which part were accessed.

```python
d[0]
```

::PROV[::GET NAME:: mapping for accesses to parts](::GET BASE::/access)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the PROV-Dictionary `derivedByInsertionFrom` to create a new version with the new part, and associate the new version to the entity that had the previous version.

Additionaly, we use the `referenceDerivedFromAccess` relationship with mode "w" to indicate that a part of a structure was changed.


```python
d[1] = 3
```

::PROV[::GET NAME:: mapping for assignments to parts](::GET BASE::/part_assign)

Comparison:

* In our mapping, we just need to create a new version. All entities that share the version through the referenceDerivedFrom keep sharing the new version.

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
