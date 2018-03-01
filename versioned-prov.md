# Versioned-Prov

In this document we map simple script constructs to Versioned-PROV.

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
entity(n1, [value="1", type="literal", label="1", generatedAtTime="2018-02-22T16:00:00"])
entity(a1, [value="'a'", type="literal", label="'a'", generatedAtTime="2018-02-22T16:00:01"])
entity(a2, [value="b'a'", type="literal", label="b'a'", generatedAtTime="2018-02-22T16:00:02"])
entity(true1, [value="True", type="constant", label="True", generatedAtTime="2018-02-22T16:00:03"])
entity(int1, [value="<class int>", type="name", label="int", generatedAtTime="2018-02-22T16:00:04"])
entity(ellipsis1, [value="Ellipsis", type="constant", label="...", generatedAtTime="2018-02-22T16:00:05"])
```


![Versioned-PROV mapping for names, literals, and constants](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/names.png)

## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value as the element on the right, we use the `referenceDerivedFrom` relationship instead of the `wasDerivedFrom`.

This relationship indicates the time of derivation and allows us to get the version of the new entity by navigating from the left side entity to the right side entity.

```python
m = 10000
```

```provn
entity(n10000, [value="10000", type="literal", label="10000", generatedAtTime="T1"])
entity(m1, [value="m", type="name", generatedAtTime="T2"])

activity(assign1, [type="assign"])
used(u1; assign1, n10000, -)
wasGeneratedBy(g1; m1, assign1, -)
referenceDerivedFrom(m1, n10000, assign1, g1, u1, T2)
```

![Versioned-PROV mapping for assignments](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/assign.png)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `wasDerivedFrom` relationship. Otherwise, we use the `referenceDerivedFrom` relationship.

```python
m + 1
```

```provn
entity(n1, [value="1", type="literal", label="1", generatedAtTime="T3"])
entity(sum1, [value="10001", type="operation", label="m + 1", generatedAtTime="T4"])

activity(add1, [type="operation"])
used(u2; add1, m1, -)
used(u3; add1, n1, -)
wasGeneratedBy(g2; sum1, add1, -)
wasDerivedFrom(sum1, m1, add1, g2, u2)
wasDerivedFrom(sum1, n1, add1, g3, u3)
```

![Versioned-PROV mapping for operations](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/operation.png)


## List definition

A list is defined by the `derivedByInsertion` relationship. This relationship indicates which items a list has at a given time.

```python
[m, m + 1, m]
```

```provn
entity(list1, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]", generatedAtTime="T5"])
derivedByInsertion(list1, {("0", n10000), ("1", sum1), ("2", n10000)}, T5)
```

![Versioned-PROV mapping for list definitions](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/list.png)

Comparison:

* In this mapping, accesses to parts indicate the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall.



## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `referenceDerivedFrom` relationship to indicate that the entity share a reference.

```python
d = [m, m + 1, m]
```

```provn
entity(d1, [value="[10000, 10001, 10000]", type="name", label="d", generatedAtTime="T6"])

activity(assign2, [type="assign"])
used(u7; assign2, list1, -)
wasGeneratedBy(g7; d1, assign2, -)
referenceDerivedFrom(d1, list1, assign2, g7, u7, T6)
```

![Versioned-PROV mapping for assignments of list definitions](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/list_assign.png)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x1, [value="[10000, 10001, 10000]", type="name", label="x", generatedAtTime="T7"])

activity(assign3, [type="assign"])
used(u8; assign3, d1, -)
wasGeneratedBy(g8; x1, assign3, -)
referenceDerivedFrom(x1, d1, assign3, g8, u8, T7)
```

![Versioned-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/list_assign2.png)

## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. 

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d1, [value="3", type="eval", label="len(d)", generatedAtTime="T8"])

activity(len1, [type="len"])
used(len1, d1, -)
wasGeneratedBy(len_d1, len1, -)
```

![Versioned-PROV mapping for function calls](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/call.png)

## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).
Additionally, the activity also has a relationship `usedPart` that indicates that it is using a specific part of an entity at a given time. The time is used to infer which version of the entity it is using, and the part is obtained from the version.

We also use the `wasDerivedFrom` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
entity(n0, [value="0", type="literal", label="0", generatedAtTime="T9"])

entity(d_ac0_1, [value="10000", type="access", label="d[0]", generatedAtTime="T10"])


activity(access1, [type="access"])
used(access1, d1, -)
used(access1, n0, -)
usedPart(u9; access1, n10000, "0", d1, T10)
wasGeneratedBy(g9; d_ac0_1, access1, -)
wasDerivedFrom(d_ac0_1, n10000, access1, g9, u9)
```

![Versioned-PROV mapping for accesses to parts](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/access.png)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We also use the `derivedByInsertion` relationship to update a list. This relationship creates a new version based on the previous one by using the timestamp.

Additionaly, we use the `usedPart` relationship for the access entity and the access entity is a referenceDerivedFrom the entity on the right side.


```python
d[1] = 3
```

```provn
entity(n3, [value="3", type="literal", label="3", generatedAtTime="T10"])
entity(n1_2, [value="1", type="literal", label="1", generatedAtTime="T11"])

entity(d_ac1_1, [value="3", type="access", label="d[1]", generatedAtTime="T12"])
derivedByInsertion(list1, {("1", d_ac1_1)}, T12)

activity(assign4, [type="assign"])
used(assign4, d1, -)
used(assign4, n1_2, -)
usedPart(u10; assign4, n3, "1", d1, T12)
wasGeneratedBy(g10; d_ac1_1, assign4, -)
referenceDerivedFrom(d_ac1_1, n3, assign4, g10, u10, T12)
```

![Versioned-PROV mapping for assignments to parts](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/part_assign.png)

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
entity(n10000, [value="10000", type="literal", label="10000", generatedAtTime="T1"])
entity(m1, [value="m", type="name", generatedAtTime="T2"])

activity(assign1, [type="assign"])
used(u1; assign1, n10000, -)
wasGeneratedBy(g1; m1, assign1, -)
referenceDerivedFrom(m1, n10000, assign1, g1, u1, T2)

// operation
entity(n1, [value="1", type="literal", label="1", generatedAtTime="T3"])
entity(sum1, [value="10001", type="operation", label="m + 1", generatedAtTime="T4"])

activity(add1, [type="operation"])
used(u2; add1, m1, -)
used(u3; add1, n1, -)
wasGeneratedBy(g2; sum1, add1, -)
wasDerivedFrom(sum1, m1, add1, g2, u2)
wasDerivedFrom(sum1, n1, add1, g3, u3)

// list def
entity(list1, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]", generatedAtTime="T5"])
derivedByInsertion(list1, {("0", n10000), ("1", sum1), ("2", n10000)}, T5)

// list assign
entity(d1, [value="[10000, 10001, 10000]", type="name", label="d", generatedAtTime="T6"])

activity(assign2, [type="assign"])
used(u7; assign2, list1, -)
wasGeneratedBy(g7; d1, assign2, -)
referenceDerivedFrom(d1, list1, assign2, g7, u7, T6)

// list assign x
entity(x1, [value="[10000, 10001, 10000]", type="name", label="x", generatedAtTime="T7"])

activity(assign3, [type="assign"])
used(u8; assign3, d1, -)
wasGeneratedBy(g8; x1, assign3, -)
referenceDerivedFrom(x1, d1, assign3, g8, u8, T7)

// call
entity(len_d1, [value="3", type="eval", label="len(d)", generatedAtTime="T8"])

activity(len1, [type="len"])
used(len1, d1, -)
wasGeneratedBy(len_d1, len1, -)

// part access
entity(n0, [value="0", type="literal", label="0", generatedAtTime="T9"])

entity(d_ac0_1, [value="10000", type="access", label="d[0]", generatedAtTime="T10"])


activity(access1, [type="access"])
used(access1, d1, -)
used(access1, n0, -)
usedPart(u9; access1, n10000, "0", d1, T10)
wasGeneratedBy(g9; d_ac0_1, access1, -)
wasDerivedFrom(d_ac0_1, n10000, access1, g9, u9)

// part assign
entity(n3, [value="3", type="literal", label="3", generatedAtTime="T10"])
entity(n1_2, [value="1", type="literal", label="1", generatedAtTime="T11"])

entity(d_ac1_1, [value="3", type="access", label="d[1]", generatedAtTime="T12"])
derivedByInsertion(list1, {("1", d_ac1_1)}, T12)

activity(assign4, [type="assign"])
used(assign4, d1, -)
used(assign4, n1_2, -)
usedPart(u10; assign4, n3, "1", d1, T12)
wasGeneratedBy(g10; d_ac1_1, assign4, -)
referenceDerivedFrom(d_ac1_1, n3, assign4, g10, u10, T12)
```

![Versioned-PROV mapping](https://github.com/dew-uff/mutable-prov/raw/master/versioned_prov/full.png)