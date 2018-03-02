# Intertwined-Prov

In this document we map simple script constructs to Intertwined-PROV.

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


```provn
entity(1, [value="1", type="literal"])
entity(1_v1, [generatedAtTime="2018-02-22T16:00:00", type="Version"])
specializationOf(1, 1_v1)

entity(a, [value="'a'", type="literal"])
entity(a_v1, [generatedAtTime="2018-02-22T16:00:01", type="Version"])
specializationOf(a, a_v1)

entity(a#2, [value="b'a'", type="literal"])
entity(a#2_v1, [generatedAtTime="2018-02-22T16:00:02", type="Version"])
specializationOf(a#2, a#2_v1)

entity(True, [value="True", type="constant"])
entity(True_v1, [generatedAtTime="2018-02-22T16:00:03", type="Version"])
specializationOf(True, True_v1)

entity(int, [value="<class 'int'>", type="name", label="int"])
entity(int_v1, [generatedAtTime="2018-02-22T16:00:04", type="Version"])
specializationOf(int, int_v1)

entity(ellipsis, [value="Ellipsis", type="constant", label="..."])
entity(ellipsis_v1, [generatedAtTime="2018-02-22T16:00:05", type="Version"])
specializationOf(ellipsis, ellipsis_v1)
```


![Intertwined-PROV mapping for names, literals, and constants](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/names.png)

## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value as the element on the right, we use the `referenceDerivedFrom` relationship instead of the `wasDerivedFrom`.

This relationship indicates the time of derivation and allows us to get the version of the new entity by navigating from the left side entity to the right side entity.

```python
m = 10000
```

```provn
entity(10000, [value="10000", type="literal"])
entity(10000_v1, [generatedAtTime="T1", type="Version"])
specializationOf(10000, 10000_v1)

entity(m, [value="10000", type="name", label="m"])

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
referenceDerivedFrom(m, 10000, assign1, g1, u1, T2)
```

![Intertwined-PROV mapping for assignments](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/assign.png)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we create a new version for it, and associate the entity to the version through the `specializationOf` relationship. Otherwise, we use the `referenceDerivedFrom` relationship.

```python
m + 1
```

```provn
entity(1, [value="1", type="literal"])
entity(1_v1, [generatedAtTime="T3", type="Version"])
specializationOf(1, 1_v1)

entity(sum, [value="10001", type="operation", label="m + 1"])
entity(sum_v1, [generatedAtTime="T4", type="Version"])
specializationOf(sum, sum_v1)

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)
```

![Intertwined-PROV mapping for operations](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/operation.png)


## List definition

A list is defined and represented by the `hadItems` relationship on the version.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]"])
entity(list_v1, [generatedAtTime="T5", type="Version"])
specializationOf(list, list_v1)
hadDictionaryMember(list_v1, m, "0")
hadDictionaryMember(list_v1, sum, "1")
hadDictionaryMember(list_v1, m, "2")
```

![Intertwined-PROV mapping for list definitions](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/list.png)

Comparison:

* The `hadItems` relationship is equivalent to a series of hadDictionaryMember relationships

* In this mapping, accesses to parts indicate the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall.



## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `referenceDerivedFrom` relationship to indicate that the entity share a reference.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="name", label="d"])

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
referenceDerivedFrom(d, list, assign2, g7, u7, T6)
```

![Intertwined-PROV mapping for assignments of list definitions](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/list_assign.png)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="name", label="x"])

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
referenceDerivedFrom(x, d, assign3, g8, u8, T7)
```

![Intertwined-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/list_assign2.png)

## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. 

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d, [value="3", type="eval", label="len(d)"])
entity(len_d_v1, [generatedAtTime="T8", type="Version"])
specializationOf(len_d, len_d_v1)

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)
```

![Intertwined-PROV mapping for function calls](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/call.png)

## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).
Additionally, the activity also has a relationship `usedPart` that indicates that it is using a specific part of an entity at a given time. The time is used to infer which version of the entity it is using, and the part is obtained from the version.

We also use the `wasDerivedFrom` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
entity(0, [value="0", type="literal"])
entity(0_v1, [generatedAtTime="T9", type="Version"])
specializationOf(0, 0_v1)

entity(d_ac0, [value="10000", type="access", label="d[0]"])


activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
usedPart(u9; access1, m, "0", d, T10)
wasGeneratedBy(g9; d_ac0, access1, -)
referenceDerivedFrom(d_ac0, m, access1, g9, u9, T9)
```

![Intertwined-PROV mapping for accesses to parts](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/access.png)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the PROV-Dictionary `derivedByInsertionFrom` to create a new version with the new part, and associate the new version to the entity that had the previous version.

Additionaly, we use the `usedPart` relationship for the access entity and the access entity is a referenceDerivedFrom the entity on the right side.


```python
d[1] = 3
```

```provn
entity(3, [value="3", type="literal"])
entity(3_v1, [generatedAtTime="T10", type="Version"])
specializationOf(3, 3_v1)

entity(1_2, [value="1", type="literal"])
entity(1_2_v1, [generatedAtTime="T11", type="Version"])
specializationOf(1_2, 1_2_v1)

entity(d_ac1, [value="3", type="access", label="d[1]"])

entity(list_v2, [generatedAtTime="T12", type="Version"])
derivedByInsertionFrom(list_v2, list_v1, {("1", d_ac1)})
specializationOf(list, list_v2)

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1_2, -)
usedPart(u10; assign4, 3, "1", d, T12)
wasGeneratedBy(g10; d_ac1, assign4, -)
referenceDerivedFrom(d_ac1, 3, assign4, g10, u10, T12)
```

![Intertwined-PROV mapping for assignments to parts](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/part_assign.png)

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

```provn
// assignment
entity(10000, [value="10000", type="literal"])
entity(10000_v1, [generatedAtTime="T1", type="Version"])
specializationOf(10000, 10000_v1)

entity(m, [value="10000", type="name", label="m"])

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
referenceDerivedFrom(m, 10000, assign1, g1, u1, T2)

// operation
entity(1, [value="1", type="literal"])
entity(1_v1, [generatedAtTime="T3", type="Version"])
specializationOf(1, 1_v1)

entity(sum, [value="10001", type="operation", label="m + 1"])
entity(sum_v1, [generatedAtTime="T4", type="Version"])
specializationOf(sum, sum_v1)

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)

// list def
entity(list, [value="[10000, 10001, 10000]", type="list", label="[m, m + 1, m]"])
entity(list_v1, [generatedAtTime="T5", type="Version"])
specializationOf(list, list_v1)
hadDictionaryMember(list_v1, m, "0")
hadDictionaryMember(list_v1, sum, "1")
hadDictionaryMember(list_v1, m, "2")

// list assign
entity(d, [value="[10000, 10001, 10000]", type="name", label="d"])

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
referenceDerivedFrom(d, list, assign2, g7, u7, T6)

// list assign x
entity(x, [value="[10000, 10001, 10000]", type="name", label="x"])

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
referenceDerivedFrom(x, d, assign3, g8, u8, T7)

// call
entity(len_d, [value="3", type="eval", label="len(d)"])
entity(len_d_v1, [generatedAtTime="T8", type="Version"])
specializationOf(len_d, len_d_v1)

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="literal"])
entity(0_v1, [generatedAtTime="T9", type="Version"])
specializationOf(0, 0_v1)

entity(d_ac0, [value="10000", type="access", label="d[0]"])

activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
usedPart(u9; access1, m, "0", d, T10)
wasGeneratedBy(g9; d_ac0, access1, -)
referenceDerivedFrom(d_ac0, m, access1, g9, u9, T9)

// part assign
entity(3, [value="3", type="literal"])
entity(3_v1, [generatedAtTime="T10", type="Version"])
specializationOf(3, 3_v1)

entity(1#2, [value="1", type="literal"])
entity(1#2_v1, [generatedAtTime="T11", type="Version"])
specializationOf(1#2, 1#2_v1)

entity(d_ac1, [value="3", type="access", label="d[1]"])

entity(list_v2, [generatedAtTime="T12", type="Version"])
derivedByInsertionFrom(list_v2, list_v1, {("1", d_ac1)})
specializationOf(list, list_v2)

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1#2, -)
usedPart(u10; assign4, 3, "1", d, T12)
wasGeneratedBy(g10; d_ac1, assign4, -)
referenceDerivedFrom(d_ac1, 3, assign4, g10, u10, T12)
```

![Intertwined-PROV mapping](https://github.com/dew-uff/mutable-prov/raw/master/intertwined_prov/full.png)