# Versioned-PROV

In this document we map simple script constructs to Versioned-PROV.

## Extension

Versioned-PROV adds the following types to existing PROV statements:

| Type      | Statement      | Meaning                                                                                                                                                                        |
|:----------|:---------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Reference | wasDerivedFrom | The generated entity derived from the used entity by reference, indicating that both have the same members.                                                                    |
| Put       | hadMember      | The collection entity had a member at a given checkpoint. If the member is a VoidEntity or a placeholder, this operation represents a removal.                                 |
| Del       | hadMember      | The collection entity lost a member at a given checkpoint. Valid for sets (that have no key) and lists. In lists, it has the semantic of updating all indexes.                 |
| Add       | hadMember      | A member was added at a given position (key) of a list at a given checkpoint. Shifts keys that occur after the iserted key.                                                    |
| VoidEntity| entity         | Represents a void entity for removals that use the put.                                                                                                                        |

Additionally, Versioned-PROV adds the following attributes to existing PROV statements:

| Attribute  | Range          | Statement                           | Meaning                                                                                        |
|:-----------|:--------------:|:------------------------------------|------------------------------------------------------------------------------------------------|
| checkpoint | Sortable Value | hadMember                           | Checkpoint of the collection update. Required for Insertion and Removal types.                 |
| checkpoint | Sortable Value | Events (e.g., used, wasDerivedFrom) | Checkpoint of the event. Required for collections that share references.                       |
| key        | String         | hadMember                           | The position of Insertion/Removal.                                                             |
| key        | String         | wasDerivedFrom                      | The position of accessed *whole* entity.                                                       |
| whole      | Entity Id      | wasDerivedFrom                      | Collection entity that was accessed or changed.                                                |
| access     | "r" or "w"     | wasDerivedFrom                      | Indicates whether an access reads ("r") and element from a collection or writes ("w") into it. |


## Names, literals, and constants

During the script execution, function calls, literals (e.g., "a", 1, True), names, and all expressions that may produce any value are evaluations. In our mapping, we represent evaluations as `entities`.


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
prefix version <https://dew-uff.github.io/versioned-prov/ns#>
    
entity(1, [value="1", type="script:literal"])
entity(a, [value="'a'", type="script:literal"])
entity(a#2, [value="b'a'", type="script:literal"])
entity(True, [value="True", type="script:constant"])
entity(int, [value="<class 'int'>", type="script:name", label="int"])
entity(ellipsis, [value="Ellipsis", type="script:constant", label="..."])
```

[![Versioned-PROV mapping for names, literals, and constants](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/names.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/names.pdf)

## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given checkpoint.

If the element on the left side of the assignment references the same value (i.e., memory address) as the element on the right, we use the `type="version:Reference"` in the `wasDerivedFrom` statement and we also specify the `checkpoint` of the derivation. We call it a *derivation by reference*.

We can follow derivations by reference transitively to infer all the members of a derived collection entity.

The `checkpoint` attribute in a derivation indicates the version of the derived instance. This attribute has no influence for non-collection data types, but we still can use it in names, literals, and constants for uniformity in the provenance collection.

```python
m = 10000
```

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix version <https://dew-uff.github.io/versioned-prov/ns#>
    
entity(10000, [value="10000", type="script:literal"])
entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="version:Reference", version:checkpoint="1"])
```

[![Versioned-PROV mapping for assignments](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/assign.pdf)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

```python
m + 1
```

```provn
entity(1, [value="1", type="script:literal"])
entity(sum, [value="10001", type="script:eval", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2, [version:checkpoint="2"])
wasDerivedFrom(sum, 1, +, g2, u3, [version:checkpoint="2"])
```

[![Versioned-PROV mapping for operations](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/operation.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/operation.pdf)


Usually, an operation generates a different value from its operands. However, in some situations it may produce the value of an operand (e.g., `[1, 2] or [3, 4]` returns `[1, 2]`). In this case, we use a derivation by reference, by specifying `type="Reference"` and stating the `checkpoint` of `wasDerivedFrom`.

Note, however, that an entity can only have a single derivation by reference, since it is not possible for an entity to have the members of distinct values at the same time.

## List definition

A list is defined by the `hadMember` relationships with `type="version:Insertion"`. The `key` attribute indicate the position of the element in the list, and the `checkpoint` attribute indicate at which version of the list, the element became part of it.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
hadMember(list, m, [type="version:Put", version:key="0", version:checkpoint="3"])
hadMember(list, sum, [type="version:Put", version:key="1", version:checkpoint="3"])
hadMember(list, m, [type="version:Put", version:key="2", version:checkpoint="3"])
```

[![Versioned-PROV mapping for list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list.pdf)


## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use `wasDerivedFrom` with `type="Reference"` and a `checkpoint` to indicate that the variable share a reference.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="version:Reference", version:checkpoint="4"])
```

[![Versioned-PROV mapping for assignments of list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="name", label="x"])

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="version:Reference", version:checkpoint="5"])
```

[![Versioned-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list_assign2.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list_assign2.pdf)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. If the used entity is a collection, the `used` statement must have a `checkpoint` indicating which version of the collection were used.

When we do not know the function call implementation, we cannot use `wasDerivedFrom` relationships. Instead, we use only `wasGeneratedBy` and we indicate the `checkpoint`.

```python
len(d)
```

```provn
entity(len_d, [value="3", type="script:eval", label="len(d)"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -, [version:checkpoint="6"])
wasGeneratedBy(len_d, call1, -, [version:checkpoint="7"])
```

[![Versioned-PROV mapping for function call](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/call.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/call.pdf)


## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the attributes `key` and `whole` in `wasDerivedFrom` to indicate which part were accessed. Moreover, the attribute `access="r"` indicates that it was a *read* access.

```python
d[0]
```

```provn
entity(0, [value="0", type="script:literal"])

entity(d@0, [value="10000", type="script:access", label="d[0]"])
activity(access1, [type="script:access"])
used(access1, d, -, [version:checkpoint="8"])
used(access1, 0, -)
wasDerivedFrom(d@0, m, access1, g5, u6, [
    type="version:Reference", version:checkpoint="9", 
    version:whole="d", version:key="0", version:access="r"])
```

[![Versioned-PROV mapping for accesses to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/access.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/access.pdf)


## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We also use the `hadMember` relationship with type `Insertion` to update a list. This relationship is incremental, so it creates a new version based on the previous one by using the `checkpoint`. At checkpoint 15, the list has all elements it had at checkpoint 14, in addition to `hadMember` insertions that occur at checkpoint 15.

Additionaly, we use the attributes `key` and `whole` in `wasDerivedFrom` to indicate which part of which structure were changed, and the attribute `access="w"` to indicate the derivation represents also a *write* in the structure.


```python
d[1] = 3
```

```provn
entity(3, [value="3", type="script:literal"])

entity(d@1, [value="3", type="script:access", label="d[1]"])
hadMember(list, d@1, [type="version:Put", version:key="1", version:checkpoint="11"])

activity(assign4, [type="script:assign"])
used(assign4, d, -, [version:checkpoint="10"])
used(assign4, 1, -)
wasDerivedFrom(d@1, 3, assign4, g6, u7, [
    type="version:Reference", version:checkpoint="11",
    version:whole="d", version:key="1", version:access="w"])
```

[![Versioned-PROV mapping for assignments to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/part_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/part_assign.pdf)

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
prefix version <https://dew-uff.github.io/versioned-prov/ns#>

// assignment
entity(10000, [value="10000", type="script:literal"])
entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="version:Reference", version:checkpoint="1"])

// operation
entity(1, [value="1", type="script:literal"])
entity(sum, [value="10001", type="script:eval", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2, [version:checkpoint="2"])
wasDerivedFrom(sum, 1, +, g2, u3, [version:checkpoint="2"])

// list def
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
hadMember(list, m, [type="version:Put", version:key="0", version:checkpoint="3"])
hadMember(list, sum, [type="version:Put", version:key="1", version:checkpoint="3"])
hadMember(list, m, [type="version:Put", version:key="2", version:checkpoint="3"])

// list assign
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="version:Reference", version:checkpoint="4"])

// list assign x
entity(x, [value="[10000, 10001, 10000]", type="name", label="x"])

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="version:Reference", version:checkpoint="5"])

// call
entity(len_d, [value="3", type="script:eval", label="len(d)"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -, [version:checkpoint="6"])
wasGeneratedBy(len_d, call1, -, [version:checkpoint="7"])

// part access
entity(0, [value="0", type="script:literal"])

entity(d@0, [value="10000", type="script:access", label="d[0]"])
activity(access1, [type="script:access"])
used(access1, d, -, [version:checkpoint="8"])
used(access1, 0, -)
wasDerivedFrom(d@0, m, access1, g5, u6, [
    type="version:Reference", version:checkpoint="9", 
    version:whole="d", version:key="0", version:access="r"])

// part assign
entity(3, [value="3", type="script:literal"])

entity(d@1, [value="3", type="script:access", label="d[1]"])
hadMember(list, d@1, [type="version:Put", version:key="1", version:checkpoint="11"])

activity(assign4, [type="script:assign"])
used(assign4, d, -, [version:checkpoint="10"])
used(assign4, 1, -)
wasDerivedFrom(d@1, 3, assign4, g6, u7, [
    type="version:Reference", version:checkpoint="11",
    version:whole="d", version:key="1", version:access="w"])
```

[![Versioned-PROV mapping](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/full.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/full.pdf)