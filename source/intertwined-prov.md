::SET BASE = generated/intertwined_prov::
::SET NAME = Intertwined-PROV::

# ::GET NAME::

In this document we map simple script constructs to ::GET NAME::.

**This extension were discontinued in favor of [Versioned-PROV](versioned-prov.html)**

## Extension


::GET NAME:: adds the following types to existing PROV statements:

| Type      | Statement      | Meaning                                                                                                     |
|:----------|:---------------|:------------------------------------------------------------------------------------------------------------|
| Reference | wasDerivedFrom | The generated entity derived from the used entity by reference, indicating that both have the same members. |
| Version   | entity         | This type inherits from the type `Dictionary` of PROV-Dictionary. It is used to represent a version entity. |

Additionally, ::GET NAME:: adds the following attributes to existing PROV statements:

| Attribute  | Range          | Statement                           | Meaning                                                                                        |
|:-----------|:--------------:|:------------------------------------|------------------------------------------------------------------------------------------------|
| checkpoint | Sortable Value | Events (e.g., used, wasDerivedFrom) | Checkpoint of the event. Required for entities that share versions.                            |
| checkpoint | Sortable Value | entity                              | Checkpoint of version entity generation. Required for versions.                                |
| key        | String         | wasDerivedFrom                      | The position of accessed *collection* entity.                                                       |
| collection | Entity Id      | wasDerivedFrom                      | Collection entity that was accessed or changed.                                                |
| access     | "r" or "w"     | wasDerivedFrom                      | Indicates whether an access reads ("r") and element from a collection or writes ("w") into it. |


## Names, literals, and constants

During the script execution, function calls, literals (e.g., "a", 1, True), names, and all expressions that may produce any value are evaluations. In our mapping, we represent evaluations as `entities`.


All evaluation entities that represent collections must have versions. We represent versions by an entity with type `Version` and attribute `checkpoint` indicating the moment.

Versions have no effect on non-collection data types, but we still can use it for names, literals, and constants for uniformity in the provenance collection.

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

If the element on the left side of the assignment references the same value (i.e., memory address) as the element on the right, we use the `type="intertwined:Reference"` in the `wasDerivedFrom` statement and we also specify the `checkpoint` of the derivation. We call it a *derivation by reference*.

We can follow derivations by reference transitively to infer the version of a derived entity.

The `checkpoint` attribute in a derivation indicates the version of the derived instance.


```python
m = 10000
```

::PROV[::GET NAME:: mapping for assignments](::GET BASE::/assign)

## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.


```python
m + 1
```

::PROV[::GET NAME:: mapping for operations](::GET BASE::/operation)

Usually, an operation generates a different value from its operands. In this case, we create a new version for it, and associate the entity to the version through the `specializationOf` relationship. However, in some situations it may produce the value of an operand (e.g., `[1, 2] or [3, 4]` returns `[1, 2]`). In this case, we use a derivation by reference, by specifying `type="Reference"` and stating the `checkpoint` of `wasDerivedFrom`.

Note, however, that an entity can only have a single derivation by reference, since it is not possible for an entity to have the members of distinct values at the same time.


## List definition

A list is defined and represented by a series of `hadDictionaryMember` on the version, indicating which entities are the parts.

```python
[m, m + 1, m]
```

::PROV[::GET NAME:: mapping for list definitions](::GET BASE::/list)


## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use `wasDerivedFrom` with `type="Reference"` and a `checkpoint` to indicate that the variable share a reference.


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

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. If the used entity is a collection, the `used` statement must have a `checkpoint` indicating which version of the collection were used.

When we do not know the function call implementation, we cannot use `wasDerivedFrom` relationships. Instead, we use only `wasGeneratedBy` and we indicate the `checkpoint`.


```python
len(d)
```

::PROV[::GET NAME:: mapping for function call](::GET BASE::/call)

## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the attributes `key` and `collection` in `wasDerivedFrom` to indicate which part were accessed. Moreover, the attribute `access="r"` indicates that it was a *read* access.

```python
d[0]
```

::PROV[::GET NAME:: mapping for accesses to parts](::GET BASE::/access)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the PROV-Dictionary `derivedByInsertionFrom` to create a new version with the new part. We also use the `specializationOf` statement to associate the new version to the entity that had the previous version.

Additionaly, we use the attributes `key` and `collection` in `wasDerivedFrom` to indicate which part of which structure were changed, and the attribute `access="w"` to indicate the derivation represents also a *write* in the structure.


```python
d[1] = 3
```

::PROV[::GET NAME:: mapping for assignments to parts](::GET BASE::/part_assign)

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
