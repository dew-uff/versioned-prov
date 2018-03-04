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
entity(1, [label="1", type="literal"])
value(v1, [repr="1"])
defined(1, v1, 2018-02-22T16:00:00)
wasDefinedBy(v1, 1, 2018-02-22T16:00:00)

entity(a, [label="'a'", type="literal"])
value(va, [repr="'a'"])
defined(a, va, 2018-02-22T16:00:01)
wasDefinedBy(va, a, 2018-02-22T16:00:01)

entity(a#2, [label="b'a'", type="literal"])
value(vba, [repr="b'a'"])
defined(a#2, vba, 2018-02-22T16:00:02)
wasDefinedBy(vba, a#2, 2018-02-22T16:00:02)

entity(True, [label="True", type="constant"])
value(vtrue, [repr="True"])
defined(True, vtrue, 2018-02-22T16:00:03)
wasDefinedBy(vtrue, True, 2018-02-22T16:00:03)

entity(int, [label="int", type="name"])
value(vint, [repr="<class 'int'>"])
defined(int, vint, 2018-02-22T16:00:04)
wasDefinedBy(vint, int, 2018-02-22T16:00:04)

entity(ellipsis, [label="...", type="constant"])
value(vellipsis, [repr="Ellipsis"])
defined(ellipsis, vellipsis, 2018-02-22T16:00:05)
wasDefinedBy(vellipsis, ellipsis, 2018-02-22T16:00:05)
```

[![Mutable-PROV mapping for names, literals, and constants](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/names.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/names.pdf)


## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the value used by each entity in a given time.

If the element on the left side of the assignment has the same value as the element on the right, we use the `accessed` relationship instead of the `defined`.

```python
m = 10000
```

```provn
entity(10000, [label="10000", type="literal"])
value(v10000, [repr="10000"])
defined(10000, v10000, T1)
wasDefinedBy(v10000, 10000, T1)

entity(m, [label="m", type="name"])
accessed(m, v10000, T2)

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
wasDerivedFrom(m, 10000, assign1, g1, u1)
```

[![Mutable-PROV mapping for assignments](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/assign.pdf)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `defined` relationship to associate it to a `value`. Otherwise, we use the `accessed` relationship.

```python
m + 1
```

```provn
entity(1, [label="1", type="literal"])
value(v1, [repr="1"])
defined(1, v1, T3)
wasDefinedBy(v1, 1, T3)

entity(sum, [label="m + 1", type="operation"])
value(v10001, [repr="10001"])
defined(sum, v10001, T4)
wasDefinedBy(v10001, sum, T4)

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)
```

[![Mutable-PROV mapping for operations](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/operation.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/operation.pdf)


## List definition

A list is defined and represented by the `derivedByInsertion` relationship.

```python
[m, m + 1, m]
```

```provn
entity(list, [label="[m, m + 1, m]", type="list"])
value(vlist, [repr="[10000, 10001, 10000]"])
derivedByInsertion(
    list, vlist,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
defined(list, vlist, T5)
wasDefinedBy(vlist, list, T5)
```

[![Mutable-PROV mapping for list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/list.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/list.pdf)


Comparison:

* Mutable-PROV accesses to parts indicates the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall. Note however that we do not navigate from the list entity `list1` to the part entity `m1` in a derivation query. Instead, we navigate to the entity that defined the value of `m1`. We could have a similar structure to the other approaches with an activity using `m1` and `sum1` and generating `list1` without a derivation relationship to indicate this usage. Since this usage does not affect the provenance query of Floyd-Warshall, we opted to leave it out.


## Assignment of list definition

With mutable-prov, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `accessed` relationship to indicate that accessed value by the entity.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [label="d", type="name"])
accessed(d, vlist, T6)

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
wasDerivedFrom(d, list, assign2, g7, u7)
```

[![Mutable-PROV mapping for assignments of list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/list_assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [label="x", type="name"])
accessed(x, vlist, T7)

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
wasDerivedFrom(x, d, assign3, g8, u8)
```

[![Mutable-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/list_assign2.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/list_assign2.pdf)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return.

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d, [label="len(d)", type="eval"])
value(v3, [repr="3"])
defined(len_d, v3, T8)
wasDefinedBy(v3, len_d, T8)

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)
```

[![Mutable-PROV mapping for function call](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/call.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/call.pdf)


## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the `accessedPart` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
entity(0, [value="0", type="literal"])
value(v0, [repr="0"])
defined(0, v0, T9)
wasDefinedBy(v0, 0, T9)
entity(d_ac0, [label="d[0]", type="access"])
accessedPart(d_ac0, vlist, "0", v10000, T10)


activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
wasGeneratedBy(g9; d_ac0, access1, -)
```

[![Mutable-PROV mapping for accesses to parts](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/access.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/access.pdf)


## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We use the `derivedByInsertion` to update the whole value withe the new part value.


```python
d[1] = 3
```

```provn
entity(3, [label="3", type="literal"])
value(v3, [repr="3"])
defined(3, v3, T10)
wasDefinedBy(v3, 3, T10)

entity(1#2, [label="1", type="literal"])
value(v1#2, [repr="1"])
defined(1#2, v1#2, T11)
wasDefinedBy(v1#2, 1#2, T11)

entity(d_ac1, [value="d[1]", type="access"])
accessed(d_ac1, v3, T12)
derivedByInsertion(d_ac1, vlist, {("1", v3)}, T12)

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1#2, -)
used(u10; assign4, 3, -)
wasGeneratedBy(g10; d_ac1, assign4, -)
wasDerivedFrom(d_ac1, 3, assign4, g10, u10)
```

[![Mutable-PROV mapping for assignments to parts](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/part_assign.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/part_assign.pdf)

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
// assignment
entity(10000, [label="10000", type="literal"])
value(v10000, [repr="10000"])
defined(10000, v10000, T1)
wasDefinedBy(v10000, 10000, T1)

entity(m, [label="m", type="name"])
accessed(m, v10000, T2)

activity(assign1, [type="assign"])
used(u1; assign1, 10000, -)
wasGeneratedBy(g1; m, assign1, -)
wasDerivedFrom(m, 10000, assign1, g1, u1)

// operation
entity(1, [label="1", type="literal"])
value(v1, [repr="1"])
defined(1, v1, T3)
wasDefinedBy(v1, 1, T3)

entity(sum, [label="m + 1", type="operation"])
value(v10001, [repr="10001"])
defined(sum, v10001, T4)
wasDefinedBy(v10001, sum, T4)

activity(+, [type="operation"])
used(u2; +, m, -)
used(u3; +, 1, -)
wasGeneratedBy(g2; sum, +, -)
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g3, u3)

// list def
entity(list, [label="[m, m + 1, m]", type="list"])
value(vlist, [repr="[10000, 10001, 10000]"])
derivedByInsertion(
    list, vlist,
    {("0", v10000), ("1", v10001), ("2", v10000)},
    T5
)
defined(list, vlist, T5)
wasDefinedBy(vlist, list, T5)

// list assign
entity(d, [label="d", type="name"])
accessed(d, vlist, T6)

activity(assign2, [type="assign"])
used(u7; assign2, list, -)
wasGeneratedBy(g7; d, assign2, -)
wasDerivedFrom(d, list, assign2, g7, u7)

// list assign x
entity(x, [label="x", type="name"])
accessed(x, vlist, T7)

activity(assign3, [type="assign"])
used(u8; assign3, d, -)
wasGeneratedBy(g8; x, assign3, -)
wasDerivedFrom(x, d, assign3, g8, u8)

// call
entity(len_d, [label="len(d)", type="eval"])
value(v3, [repr="3"])
defined(len_d, v3, T8)
wasDefinedBy(v3, len_d, T8)

activity(call1, [type="call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="literal"])
value(v0, [repr="0"])
defined(0, v0, T9)
wasDefinedBy(v0, 0, T9)
entity(d_ac0, [label="d[0]", type="access"])
accessedPart(d_ac0, vlist, "0", v10000, T10)


activity(access1, [type="access"])
used(access1, d, -)
used(access1, 0, -)
wasGeneratedBy(g9; d_ac0, access1, -)

// part assign
entity(3, [label="3", type="literal"])
value(v3, [repr="3"])
defined(3, v3, T10)
wasDefinedBy(v3, 3, T10)

entity(1#2, [label="1", type="literal"])
value(v1#2, [repr="1"])
defined(1#2, v1#2, T11)
wasDefinedBy(v1#2, 1#2, T11)

entity(d_ac1, [value="d[1]", type="access"])
accessed(d_ac1, v3, T12)
derivedByInsertion(d_ac1, vlist, {("1", v3)}, T12)

activity(assign4, [type="assign"])
used(assign4, d, -)
used(assign4, 1#2, -)
used(u10; assign4, 3, -)
wasGeneratedBy(g10; d_ac1, assign4, -)
wasDerivedFrom(d_ac1, 3, assign4, g10, u10)
```

[![Mutable-PROV mapping](https://github.com/dew-uff/mutable-prov/raw/master/images/mutable_prov/full.png)](https://github.com/dew-uff/mutable-prov/blob/master/images/mutable_prov/full.pdf)