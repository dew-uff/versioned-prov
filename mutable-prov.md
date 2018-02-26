# Mutable-PROV

In this document we map simple script constructs to Mutable-PROV.

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


```provn
entity(n1, [value="1", type="literal"])
value(v1, [repr="1"])
defined(n1, v1, 2018-02-22T16:00:00)
wasDefinedBy(v1, n1, 2018-02-22T16:00:00)

entity(a1, [value="'a'", type="literal"])
value(va, [repr="'a'"])
defined(a1, va, 2018-02-22T16:00:01)
wasDefinedBy(va, a1, 2018-02-22T16:00:01)

entity(a2, [value="b'a'", type="literal"])
value(vba, [repr="b'a'"])
defined(a2, vba, 2018-02-22T16:00:02)
wasDefinedBy(vba, a2, 2018-02-22T16:00:02)

entity(true1, [value="True", type="constant"])
value(vtrue, [repr="True"])
defined(true1, vtrue, 2018-02-22T16:00:03)
wasDefinedBy(vtrue, true1, 2018-02-22T16:00:03)

entity(int1, [value="int", type="name"])
value(vint, [repr="<class 'int'>"])
defined(int1, vint, 2018-02-22T16:00:04)
wasDefinedBy(vint, int1, 2018-02-22T16:00:04)

entity(ellipsis1, [value="...", type="constant"])
value(vellipsis, [repr="Ellipsis"])
defined(ellipsis1, vellipsis, 2018-02-22T16:00:05)
wasDefinedBy(vellipsis, ellipsis1, 2018-02-22T16:00:05)
```


![Mutable-PROV mapping for names, literals, and constants](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/names.png)

Comparison:

* Different from the other mappings, we use the attribute `value` of the `entity` to indicate its textual construct. In other mappings, we use the `value` to indicate the immutable state of an `entity`.


## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the value used by each entity in a given time.

If the element on the left side of the assignment has the same value as the element on the right, we use the `accessed` relationship instead of the `defined`.

```python
m = 10000
```

```provn
entity(n10000, [value="10000", type="literal"])
value(v10000, [repr="10000"])
defined(n10000, v10000, T1)
wasDefinedBy(v10000, n10000, T1)

entity(m1, [value="m", type="name"])
accessed(m1, v10000, T2)

activity(assign1, [type="assign"])
used(u1; assign1, n10000, -)
wasGeneratedBy(g1; m1, assign1, -)
wasDerivedFrom(m1, n10000, assign1, g1, u1)
```

![Mutable-PROV mapping for assignments](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/assign.png)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `defined` relationship to associate it to a `value`. Otherwise, we use the `accessed` relationship.

```python
m + 1
```

```provn
entity(m1, [value="10000", type="name"])
value(v10000, [repr="10000"])
accessed(m1, v10000, T2)
entity(n1, [value="1", type="literal"])
value(v1, [repr="1"])
defined(n1, v1, T3)
wasDefinedBy(v1, n1, T3)
entity(sum1, [value="m + 1", type="sum"])
value(v10001, [repr="10001"])
defined(sum1, v10001, T4)
wasDefinedBy(v10001, sum1, T4)

activity(add1, [type="add"])
used(u2; add1, m1, -)
used(u3; add1, n1, -)
wasGeneratedBy(g2; sum1, add1, -)
wasDerivedFrom(sum1, m1, add1, g2, u2)
wasDerivedFrom(sum1, n1, add1, g3, u3)
```

![Mutable-PROV mapping for operations](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/operation.png)


## List definition

A list is defined and represented by the `derivedByInsertion` relationship.

```python
[m, m + 1, m]
```

```provn
entity(m1, [value="10000", type="name"])
value(v10000, [repr="10000"])
accessed(m1, v10000, T2)

entity(sum1, [value="10001", type="sum"])
value(v10001, [repr="10001"])
defined(sum1, v10001, T4)
wasDefinedBy(v10001, sum1, T4)

entity(list1, [value="[m, m + 1, m]", type="list"])
value(vlist1, [repr="[10000, 10001, 10000]"])
derivedByInsertion(
    list1, vlist1,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
defined(list1, vlist1, T5)
wasDefinedBy(vlist1, list1, T5)
```

![Mutable-PROV mapping for list definitions](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/list.png)

Comparison:

* Mutable-PROV accesses to parts indicates the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall. Note however that we do not navigate from the list entity `list1` to the part entity `m1` in a derivation query. Instead, we navigate to the entity that defined the value of `m1`. We could have a similar structure to the other approaches with an activity using `m1` and `sum1` and generating `list1` without a derivation relationship to indicate this usage. Since this usage does not affect the provenance query of Floyd-Warshall, we opted to leave it out.



## Assignment of list definition

With mutable-prov, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `accessed` relationship to indicate that accessed value by the entity.

```python
d = [m, m + 1, m]
```

```provn
// old entities from previous figure
entity(list1, [value="[m, m + 1, m]", type="list"])
value(vlist1, [repr="[10000, 10001, 10000]"])
defined(list1, vlist1, T5)
wasDefinedBy(vlist1, list1, T5)

// new entities
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)

activity(assign2, [type="assign"])
used(u7; assign2, list1, -)
wasGeneratedBy(g7; d1, assign2, -)
wasDerivedFrom(d1, list1, assign2, g7, u7)
```

![Mutable-PROV mapping for assignments of list definitions](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/list_assign.png)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
// old entities from previous figure
value(vlist1, [repr="[10000, 10001, 10000]"])
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)

// new entities
entity(x1, [value="x", type="name"])
accessed(x1, vlist1, T7)

activity(assign3, [type="assign"])
used(u8; assign3, d1, -)
wasGeneratedBy(g8; x1, assign3, -)
wasDerivedFrom(x1, d1, assign3, g8, u8)
```

![Mutable-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/list_assign2.png)

## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return. 

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
value(vlist1, [repr="[10000, 10001, 10000]"])
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)


entity(len_d1, [value="len(d)", type="eval"])
value(v3, [repr="3"])
defined(len_d1, v3, T8)
wasDefinedBy(v3, len_d1, T8)

activity(len1, [type="len"])
used(len1, d1, -)
wasGeneratedBy(len_d1, len1, -)
```

![Mutable-PROV mapping for function calls](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/call.png)

## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`). 

We also use the `accessedPart` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
//previous
value(vlist1, [repr="[10000, 10001, 10000]"])
value(v10000, [repr="10000"])
value(v10001, [repr="10001"])
derivedByInsertion(
    -, // list1
    vlist1,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)


//access
entity(n0, [value="0", type="literal"])
value(v0, [repr="0"])
defined(n0, v0, T9)
wasDefinedBy(v0, n0, T9)
entity(d_ac0_1, [value="d[0]", type="access"])
accessedPart(d_ac0_1, vlist1, "0", v10000, T10)


activity(access1, [type="access"])
used(access1, d1, -)
used(access1, n0, -)
wasGeneratedBy(g9; d_ac0_1, access1, -)
```

![Mutable-PROV mapping for accesses to parts](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/access.png)

## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the `derivedByInsertion` to update the whole value withe the new part value.


```python
d[1] = 3
```

```provn
//previous
value(vlist1, [repr="[10000, 10001, 10000]"])
value(v10000, [repr="10000"])
value(v10001, [repr="10001"])
derivedByInsertion(
    -, // list1
    vlist1,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)


//part assign

entity(n3, [value="3", type="literal"])
value(v3, [repr="3"])
defined(n3, v3, T10)
wasDefinedBy(v3, n3, T10)

entity(n1, [value="1", type="literal"])
value(v1, [repr="1"])
defined(n1, v1, T11)
wasDefinedBy(v1, n1, T11)

entity(d_ac1_1, [value="d[1]", type="access"])
accessed(d_ac1_1, v3, T12)
derivedByInsertion(d_ac1_1, vlist1, {("1", v3)}, T12)

activity(assign4, [type="assign"])
used(assign4, d1, -)
used(assign4, n1, -)
used(u10; assign4, n3, -)
wasGeneratedBy(g10; d_ac1_1, assign4, -)
wasDerivedFrom(d_ac1_1, n3, assign4, g10, u10)
```

![Mutable-PROV mapping for assignments to parts](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/part_assign.png)

Comparison:

* With Mutable-PROV, we just need to update the `value`. All entities that `accessed` the value keep the same

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
%%provn -o ../mutable_prov/full -e png svg pdf provn
// assignment
entity(n10000, [value="10000", type="literal"])
value(v10000, [repr="10000"])
defined(n10000, v10000, T1)
wasDefinedBy(v10000, n10000, T1)

entity(m1, [value="m", type="name"])
accessed(m1, v10000, T2)

activity(assign1, [type="assign"])
used(u1; assign1, n10000, -)
wasGeneratedBy(g1; m1, assign1, -)
wasDerivedFrom(m1, n10000, assign1, g1, u1)

// operation
entity(n1, [value="1", type="literal"])
value(v1, [repr="1"])
defined(n1, v1, T3)
wasDefinedBy(v1, n1, T3)
entity(sum1, [value="m + 1", type="sum"])
value(v10001, [repr="10001"])
defined(sum1, v10001, T4)
wasDefinedBy(v10001, sum1, T4)

activity(add1, [type="add"])
used(u2; add1, m1, -)
used(u3; add1, n1, -)
wasGeneratedBy(g2; sum1, add1, -)
wasDerivedFrom(sum1, m1, add1, g2, u2)
wasDerivedFrom(sum1, n1, add1, g3, u3)

// list def

entity(list1, [value="[m, m + 1, m]", type="list"])
value(vlist1, [repr="[10000, 10001, 10000]"])
derivedByInsertion(
    list1, vlist1,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
defined(list1, vlist1, T5)
wasDefinedBy(vlist1, list1, T5)

// list assign
entity(d1, [value="d", type="name"])
accessed(d1, vlist1, T6)

activity(assign2, [type="assign"])
used(u7; assign2, list1, -)
wasGeneratedBy(g7; d1, assign2, -)
wasDerivedFrom(d1, list1, assign2, g7, u7)

// list assign x
entity(x1, [value="x", type="name"])
accessed(x1, vlist1, T7)

activity(assign3, [type="assign"])
used(u8; assign3, d1, -)
wasGeneratedBy(g8; x1, assign3, -)
wasDerivedFrom(x1, d1, assign3, g8, u8)

// call
entity(len_d1, [value="len(d)", type="eval"])
value(v3r, [repr="3"])
defined(len_d1, v3r, T8)
wasDefinedBy(v3r, len_d1, T8)

activity(len1, [type="len"])
used(len1, d1, -)
wasGeneratedBy(len_d1, len1, -)

// part access
entity(n0, [value="0", type="literal"])
value(v0, [repr="0"])
defined(n0, v0, T9)
wasDefinedBy(v0, n0, T9)
entity(d_ac0_1, [value="d[0]", type="access"])
accessedPart(d_ac0_1, vlist1, "0", v10000, T10)


activity(access1, [type="access"])
used(access1, d1, -)
used(access1, n0, -)
wasGeneratedBy(g9; d_ac0_1, access1, -)

// part assign

entity(n3, [value="3", type="literal"])
value(v3, [repr="3"])
defined(n3, v3, T10)
wasDefinedBy(v3, n3, T10)

entity(d_ac1_1, [value="d[1]", type="access"])
accessed(d_ac1_1, v3, T12)
derivedByInsertion(d_ac1_1, vlist1, {("1", v3)}, T12)

activity(assign4, [type="assign"])
used(assign4, d1, -)
used(assign4, n1, -)
used(u10; assign4, n3, -)
wasGeneratedBy(g10; d_ac1_1, assign4, -)
wasDerivedFrom(d_ac1_1, n3, assign4, g10, u10)
```

![Mutable-PROV mapping](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/full.png)