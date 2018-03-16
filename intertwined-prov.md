# Intertwined-PROV

In this document we map simple script constructs to Intertwined-PROV.

**This extension were discontinued in favor of [Versioned-PROV](versioned-prov.md)**

## Extension


Intertwined-PROV adds the following types to existing PROV statements:

| Type      | Statement      | Meaning                                                                                                     |
|:----------|:---------------|:------------------------------------------------------------------------------------------------------------|
| Reference | wasDerivedFrom | The generated entity derived from the used entity by reference, indicating that both have the same members. |
| Version   | entity         | This type inherits from the type `Dictionary` of PROV-Dictionary. It is used to represent a version entity. |

Additionally, Intertwined-PROV adds the following attributes to existing PROV statements:

| Attribute  | Range          | Statement                           | Meaning                                                                                        |
|:-----------|:--------------:|:------------------------------------|------------------------------------------------------------------------------------------------|
| checkpoint | Sortable Value | Events (e.g., used, wasDerivedFrom) | Checkpoint of the event. Required for entities that share versions.                            |
| checkpoint | Sortable Value | entity                              | Checkpoint of version entity generation. Required for versions.                                |
| key        | String         | wasDerivedFrom                      | The position of accessed *whole* entity.                                                       |
| whole      | Entity Id      | wasDerivedFrom                      | Collection entity that was accessed or changed.                                                |
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

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix intertwined <https://dew-uff.github.io/versioned-prov/ns/intertwined#>
    
entity(1, [value="1", type="script:literal"])
entity(1_v1, [intertwined:checkpoint="2018-02-22T16:00:00", type="intertwined:Version"])
specializationOf(1, 1_v1)

entity(a, [value="'a'", type="script:literal"])
entity(a_v1, [intertwined:checkpoint="2018-02-22T16:00:01", type="intertwined:Version"])
specializationOf(a, a_v1)

entity(a#2, [value="b'a'", type="script:literal"])
entity(a#2_v1, [intertwined:checkpoint="2018-02-22T16:00:02", type="intertwined:Version"])
specializationOf(a#2, a#2_v1)

entity(True, [value="True", type="script:constant"])
entity(True_v1, [intertwined:checkpoint="2018-02-22T16:00:03", type="intertwined:Version"])
specializationOf(True, True_v1)

entity(int, [value="<class 'int'>", type="script:name", label="int"])
entity(int_v1, [intertwined:checkpoint="2018-02-22T16:00:04", type="intertwined:Version"])
specializationOf(int, int_v1)

entity(ellipsis, [value="Ellipsis", type="script:constant", label="..."])
entity(ellipsis_v1, [intertwined:checkpoint="2018-02-22T16:00:05", type="intertwined:Version"])
specializationOf(ellipsis, ellipsis_v1)
```

[![Intertwined-PROV mapping for names, literals, and constants](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/names.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/names.pdf)

## Assignment


We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value (i.e., memory address) as the element on the right, we use the `type="intertwined:Reference"` in the `wasDerivedFrom` statement and we also specify the `checkpoint` of the derivation. We call it a *derivation by reference*.

We can follow derivations by reference transitively to infer the version of a derived entity.

The `checkpoint` attribute in a derivation indicates the version of the derived instance.


```python
m = 10000
```

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix intertwined <https://dew-uff.github.io/versioned-prov/ns/intertwined#>

entity(10000, [value="10000", type="script:literal"])
entity(10000_v1, [intertwined:checkpoint="1", type="intertwined:Version"])
specializationOf(10000, 10000_v1)

entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="intertwined:Reference", intertwined:checkpoint="2"])
```

[![Intertwined-PROV mapping for assignments](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/assign.pdf)

## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.


```python
m + 1
```

```provn
entity(1, [value="1", type="script:literal"])
entity(1_v1, [intertwined:checkpoint="3", type="intertwined:Version"])
specializationOf(1, 1_v1)

entity(sum, [value="10001", type="script:eval", label="m + 1"])
entity(sum_v1, [intertwined:checkpoint="4", type="intertwined:Version"])
specializationOf(sum, sum_v1)

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)
```

[![Intertwined-PROV mapping for operations](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/operation.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/operation.pdf)

Usually, an operation generates a different value from its operands. In this case, we create a new version for it, and associate the entity to the version through the `specializationOf` relationship. However, in some situations it may produce the value of an operand (e.g., `[1, 2] or [3, 4]` returns `[1, 2]`). In this case, we use a derivation by reference, by specifying `type="Reference"` and stating the `checkpoint` of `wasDerivedFrom`.

Note, however, that an entity can only have a single derivation by reference, since it is not possible for an entity to have the members of distinct values at the same time.


## List definition

A list is defined and represented by a series of `hadDictionaryMember` on the version, indicating which entities are the parts.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
entity(list_v1, [intertwined:checkpoint="5", type="intertwined:Version"])
specializationOf(list, list_v1)
hadDictionaryMember(list_v1, m, "0")
hadDictionaryMember(list_v1, sum, "1")
hadDictionaryMember(list_v1, m, "2")
```

[![Intertwined-PROV mapping for list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/list.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/list.pdf)


## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use `wasDerivedFrom` with `type="Reference"` and a `checkpoint` to indicate that the variable share a reference.


```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="intertwined:Reference", intertwined:checkpoint="6"])
```

[![Intertwined-PROV mapping for assignments of list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/list_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="script:name", label="x"])

activity(assign3, [type="assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="intertwined:Reference", intertwined:checkpoint="7"])
```

[![Intertwined-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/list_assign2.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/list_assign2.pdf)

## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. If the used entity is a collection, the `used` statement must have a `checkpoint` indicating which version of the collection were used.

When we do not know the function call implementation, we cannot use `wasDerivedFrom` relationships. Instead, we use only `wasGeneratedBy` and we indicate the `checkpoint`.


```python
len(d)
```

```provn
entity(len_d, [value="3", type="script:eval", label="len(d)"])
entity(len_d_v1, [intertwined:checkpoint="9", type="intertwined:Version"])
specializationOf(len_d, len_d_v1)

activity(call1, [type="intertwined:call", label="len"])
used(call1, d, -, [intertwined:checkpoint="8"])
wasGeneratedBy(len_d, call1, -, [intertwined:checkpoint="9"])
```

[![Intertwined-PROV mapping for function call](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/call.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/call.pdf)

## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the attributes `key` and `whole` in `wasDerivedFrom` to indicate which part were accessed. Moreover, the attribute `access="r"` indicates that it was a *read* access.

```python
d[0]
```

```provn
entity(0, [value="0", type="script:literal"])
entity(0_v1, [intertwined:checkpoint="10", type="intertwined:Version"])
specializationOf(0, 0_v1)

entity(d_ac0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="access"])
used(access1, d, -, [intertwined:checkpoint="11"])
used(access1, 0, -)
wasDerivedFrom(d_ac0, m, access1, g5, u6, [
    type="intertwined:Reference", intertwined:checkpoint="12",
    intertwined:whole="d", intertwined:key="0", intertwined:access="r"])
```

[![Intertwined-PROV mapping for accesses to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/access.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/access.pdf)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the PROV-Dictionary `derivedByInsertionFrom` to create a new version with the new part. We also use the `specializationOf` statement to associate the new version to the entity that had the previous version.

Additionaly, we use the attributes `key` and `whole` in `wasDerivedFrom` to indicate which part of which structure were changed, and the attribute `access="w"` to indicate the derivation represents also a *write* in the structure.


```python
d[1] = 3
```

```provn
entity(3, [value="3", type="script:literal"])
entity(3_v1, [intertwined:checkpoint="13", type="intertwined:Version"])
specializationOf(3, 3_v1)

entity(d_ac1, [value="3", type="script:access", label="d[1]"])

entity(list_v2, [intertwined:checkpoint="15", type="intertwined:Version"])
derivedByInsertionFrom(list_v2, list_v1, {("1", d_ac1)})
specializationOf(list, list_v2)

activity(assign4, [type="script:assign"])
used(assign4, d, -, [intertwined:checkpoint="14"])
used(assign4, 1, -)
wasDerivedFrom(d_ac1, 3, assign4, g6, u7, [
    type="intertwined:Reference", intertwined:checkpoint="15", intertwined:whole="d",
    intertwined:key="1", intertwined:access="w"])
```

[![Intertwined-PROV mapping for assignments to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/part_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/part_assign.pdf)

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

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix intertwined <https://dew-uff.github.io/versioned-prov/ns/intertwined#>

// assignment
entity(10000, [value="10000", type="script:literal"])
entity(10000_v1, [intertwined:checkpoint="1", type="intertwined:Version"])
specializationOf(10000, 10000_v1)

entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="intertwined:Reference", intertwined:checkpoint="2"])

// operation
entity(1, [value="1", type="script:literal"])
entity(1_v1, [intertwined:checkpoint="3", type="intertwined:Version"])
specializationOf(1, 1_v1)

entity(sum, [value="10001", type="script:eval", label="m + 1"])
entity(sum_v1, [intertwined:checkpoint="4", type="intertwined:Version"])
specializationOf(sum, sum_v1)

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)

// list def
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
entity(list_v1, [intertwined:checkpoint="5", type="intertwined:Version"])
specializationOf(list, list_v1)
hadDictionaryMember(list_v1, m, "0")
hadDictionaryMember(list_v1, sum, "1")
hadDictionaryMember(list_v1, m, "2")

// list assign
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="intertwined:Reference", intertwined:checkpoint="6"])

// list assign x
entity(x, [value="[10000, 10001, 10000]", type="script:name", label="x"])

activity(assign3, [type="assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="intertwined:Reference", intertwined:checkpoint="7"])

// call
entity(len_d, [value="3", type="script:eval", label="len(d)"])
entity(len_d_v1, [intertwined:checkpoint="8", type="intertwined:Version"])
specializationOf(len_d, len_d_v1)

activity(call1, [type="intertwined:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="script:literal"])
entity(0_v1, [intertwined:checkpoint="9", type="intertwined:Version"])
specializationOf(0, 0_v1)

entity(d_ac0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d_ac0, m, access1, g5, u6, [
    type="intertwined:Reference", intertwined:checkpoint="10",
    intertwined:whole="d", intertwined:key="0", intertwined:access="r"])

// part assign
entity(3, [value="3", type="script:literal"])
entity(3_v1, [intertwined:checkpoint="10", type="intertwined:Version"])
specializationOf(3, 3_v1)

entity(d_ac1, [value="3", type="script:access", label="d[1]"])

entity(list_v2, [intertwined:checkpoint="11", type="intertwined:Version"])
derivedByInsertionFrom(list_v2, list_v1, {("1", d_ac1)})
specializationOf(list, list_v2)

activity(assign4, [type="script:assign"])
used(assign4, d, -)
used(assign4, 1, -)
wasDerivedFrom(d_ac1, 3, assign4, g6, u7, [
    type="intertwined:Reference", intertwined:checkpoint="11", intertwined:whole="d",
    intertwined:key="1", intertwined:access="w"])
```

[![Intertwined-PROV mapping](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/full.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/full.pdf)

# Floyd-Warshall

This mapping produced the following graph for Floyd-Warshall:

[![Floyd-Warshall in Intertwined-PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/floydwarshall.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/floydwarshall.pdf)

# Query

The Intertwined-PROV mapping produces the following query result:

[![Query in Intertwined-PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/intertwined_prov/query.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/intertwined_prov/query.pdf)