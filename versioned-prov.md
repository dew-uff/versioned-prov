# Versioned-PROV

In this document we map simple script constructs to Versioned-PROV.

## Extension

Our extension adds new attributes to existing statements:

| Statement      | Attribute    | Values                       | Required                      |
|:--------------:|:------------:|:----------------------------:|:-----------------------------:|
| wasDerivedFrom | moment       | timestamp                    | If type is "Reference"        |
| wasDerivedFrom | type         | "Reference"                  | No                            |
| wasDerivedFrom | access       | "r" &#124; "w"               | No                            |
| wasDerivedFrom | whole        | entity id                    | If it is an access            |
| wasDerivedFrom | key          | string                       | If it is an access            |
| hadMember      | type         | "Insertion" &#124; "Removal" | No                            |
| hadMember      | moment       | timestamp                    | if type is from the extension |
| hadMember      | key          | string                       | if type is from the extension |

While we use `hadMember` with `type="Removal"` for removing elements from a data structure, the element `entity` could be empty or a reference to a void `entity`.

## Names, literals, and constants

During the script execution, function calls, literals (e.g., "a", 1, True), names, and all expressions that may produce any value are evaluations. In our mapping, we represent evaluations as `entities`.

All entities are generated at a time, we indicate the time by the `generatedAtTime` attribute.


```python
1     # literal
"a"   # literal
b"a"  # literal
True  # literal
int   # names
...   # constant
```

```provn
entity(1, [value="1", type="literal", generatedAtTime="2018-02-22T16:00:00"])
entity(a, [value="'a'", type="literal", generatedAtTime="2018-02-22T16:00:01"])
entity(a#2, [value="b'a'", type="literal", generatedAtTime="2018-02-22T16:00:02"])
entity(True, [value="True", type="constant", generatedAtTime="2018-02-22T16:00:03"])
entity(int, [value="<class 'int'>", type="name", label="int", generatedAtTime="2018-02-22T16:00:04"])
entity(ellipsis, [value="Ellipsis", type="constant", label="...", generatedAtTime="2018-02-22T16:00:05"])
```

[![Versioned-PROV mapping for names, literals, and constants](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/names.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/names.pdf)


## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value as the element on the right, we use the `referenceDerivedFrom` relationship instead of the `wasDerivedFrom`.

This relationship indicates the time of derivation and allows us to get the version of the new entity by navigating from the left side entity to the right side entity.

```python
m = 10000
```

```provn
entity(10000, [value="10000", type="literal", generatedAtTime="T1"])
entity(m, [value="10000", type="name", label="m", generatedAtTime="T2"])

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="Reference", moment="T2"])
```

[![Versioned-PROV mapping for assignments](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/assign.pdf)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `wasDerivedFrom` relationship. Otherwise, we use the `referenceDerivedFrom` relationship.

```python
m + 1
```

```provn
entity(1, [value="1", type="literal",  generatedAtTime="T3"])
entity(sum, [value="10001", type="operation", label="m + 1", generatedAtTime="T4"])

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)
```

[![Versioned-PROV mapping for operations](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/operation.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/operation.pdf)


## List definition

A list is defined by the `derivedByInsertion` relationship. This relationship indicates which items a list has at a given time.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]", generatedAtTime="T5"])
hadMember(list, m, [type="Insertion", key="0", moment="T5"])
hadMember(list, sum, [type="Insertion", key="1", moment="T5"])
hadMember(list, m, [type="Insertion", key="2", moment="T5"])
```

[![Versioned-PROV mapping for list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/list.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/list.pdf)


Comparison:

* In this mapping, accesses to parts indicate the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall.



## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `referenceDerivedFrom` relationship to indicate that the entity share a reference.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="name", label="d", generatedAtTime="T6"])

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
wasDerivedFrom(d, list, assign2, g7, u7, [type="Reference", moment="T6"])
```

[![Versioned-PROV mapping for assignments of list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/list_assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="name", label="x", generatedAtTime="T7"])

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
wasDerivedFrom(x, d, assign3, g8, u8, [type="Reference", moment="T7"])
```

[![Versioned-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/list_assign2.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/list_assign2.pdf)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return.

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d, [value="3", type="eval", label="len(d)", generatedAtTime="T8"])

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)
```

[![Versioned-PROV mapping for function call](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/call.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/call.pdf)


## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the `referenceDerivedFromAccess` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
entity(0, [value="0", type="literal", generatedAtTime="T9"])

entity(d_ac0, [value="10000", type="access", label="d[0]", generatedAtTime="T10"])


activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
used(u9; access1, m, -)
wasGeneratedBy(g9; d_ac0, access1, -)
wasDerivedFrom(d_ac0, m, access1, g9, u9, [type="Reference", moment="T10", whole="d", key="0", access="r"])
```

[![Versioned-PROV mapping for accesses to parts](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/access.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/access.pdf)


## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We also use the `derivedByInsertion` relationship to update a list. This relationship creates a new version based on the previous one by using the timestamp.

Additionaly, we use the `referenceDerivedFromAccess` relationship to indicate that a part of a structure was changed.


```python
d[1] = 3
```

```provn
entity(3, [value="3", type="literal", generatedAtTime="T10"])
entity(1#2, [value="1", type="literal", generatedAtTime="T11"])

entity(d_ac1, [value="3", type="access", label="d[1]", generatedAtTime="T12"])
hadMember(list, d_ac1, [type="Insertion", key="1", moment="T12"])

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1#2, -)
used(u10; assign4, 3)
wasGeneratedBy(g10; d_ac1, assign4, -)
wasDerivedFrom(d_ac1, 3, assign4, g10, u10, [type="Reference", moment="T12", whole="d", key="1", access="w"])
```

[![Versioned-PROV mapping for assignments to parts](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/part_assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/part_assign.pdf)

Comparison:

* In our mapping, we just need to use the `derivedByInsertion` relationship to create a new version. All entities that share the version through the referenceDerivedFrom keep sharing the new version.

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
// assignment
entity(10000, [value="10000", type="literal", generatedAtTime="T1"])
entity(m, [value="10000", type="name", label="m", generatedAtTime="T2"])

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="Reference", moment="T2"])

// operation
entity(1, [value="1", type="literal",  generatedAtTime="T3"])
entity(sum, [value="10001", type="operation", label="m + 1", generatedAtTime="T4"])

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)

// list def
entity(list, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]", generatedAtTime="T5"])
hadMember(list, m, [type="Insertion", key="0", moment="T5"])
hadMember(list, sum, [type="Insertion", key="1", moment="T5"])
hadMember(list, m, [type="Insertion", key="2", moment="T5"])

// list assign
entity(d, [value="[10000, 10001, 10000]", type="name", label="d", generatedAtTime="T6"])

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
wasDerivedFrom(d, list, assign2, g7, u7, [type="Reference", moment="T6"])

// list assign x
entity(x, [value="[10000, 10001, 10000]", type="name", label="x", generatedAtTime="T7"])

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
wasDerivedFrom(x, d, assign3, g8, u8, [type="Reference", moment="T7"])

// call
entity(len_d, [value="3", type="eval", label="len(d)", generatedAtTime="T8"])

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="literal", generatedAtTime="T9"])

entity(d_ac0, [value="10000", type="access", label="d[0]", generatedAtTime="T10"])


activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
used(u9; access1, m, -)
wasGeneratedBy(g9; d_ac0, access1, -)
wasDerivedFrom(d_ac0, m, access1, g9, u9, [type="Reference", moment="T10", whole="d", key="0", access="r"])

// part assign
entity(3, [value="3", type="literal", generatedAtTime="T10"])
entity(1#2, [value="1", type="literal", generatedAtTime="T11"])

entity(d_ac1, [value="3", type="access", label="d[1]", generatedAtTime="T12"])
hadMember(list, d_ac1, [type="Insertion", key="1", moment="T12"])

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1#2, -)
used(u10; assign4, 3)
wasGeneratedBy(g10; d_ac1, assign4, -)
wasDerivedFrom(d_ac1, 3, assign4, g10, u10, [type="Reference", moment="T12", whole="d", key="1", access="w"])
```

[![Versioned-PROV mapping](https://github.com/dew-uff/mutable-prov/raw/master/images/versioned_prov/full.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/versioned_prov/full.pdf)