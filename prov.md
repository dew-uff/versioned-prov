# PROV

In this document we map simple script constructs to plain PROV.

## Names, literals, and constants

`entities` represent variables names, literals (e.g., "a", 1, True), and constants (e.g., `...`).

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

entity(1, [value="1", type="script:literal"])
entity(a, [value="'a'", type="script:literal"])
entity(a#2, [value="b'a'", type="script:literal"])
entity(True, [prov:value="True", type="script:constant"])
entity(int, [prov:value="<class 'int'>", type="script:name", label="int"])
entity(ellipsis, [prov:value="Ellipsis", type="script:constant", label="..."])
```

[![PROV mapping for names, literals, and constants](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/names.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/names.pdf)


## Assignment

We represent an assignment by an `activity` that uses the `entities` on the right side to generate an `entity` on the left side.

An assignment creates a new entity for the name on the left side even when the name already exists.

```python
m = 10000
```

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>

entity(10000, [value="10000", type="script:literal"])
entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1)
```

[![PROV mapping for assignments](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/assign.pdf)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

```python
m + 1
```

```provn
entity(1, [value="1", type="script:literal"])
entity(sum, [value="10001", type="script:sum", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)
```

[![PROV mapping for operations](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/operation.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/operation.pdf)


## List definition

A list is represented by an `entity` with `hadMember` relationships to its parts.


The provenance of a `Floyd-Warshall` execution should indicate the position of accessed elements in the result matrix (list of lists) to allow the querying of the shortest-path between two nodes. However, using just the `hadMember` relationship, we cannot know in which position of the list a member exists (note below that an `entity` may repeat in multiple positions). Thus, to allow this query, we create an extra `entity` for every position in the list and we use an `activity` to derive these `entities` from the actual `entities` that compose the list.

For simplicity, in the case of the definition of matrices, we use a single `activity` to represent all the derivations, instead of an `activity` for each row.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
entity(list0, [value="10000", type="script:item", label="m"])
entity(list1, [value="10001", type="script:item", label="m + 1"])
entity(list2, [value="10000", type="script:item", label="m"])

hadMember(list, list0)
hadMember(list, list1)
hadMember(list, list2)

activity(definelist1, [type="script:definelist"])
wasDerivedFrom(list0, m, definelist1, g3, u4)
wasDerivedFrom(list1, sum, definelist1, g4, u5)
wasDerivedFrom(list2, m, definelist1, g5, u6)
wasGeneratedBy(list, definelist1, -)
```

[![PROV mapping for list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/list.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/list.pdf)


## Assignment of list definition

When we assign a list definition to a variable, we must create new entities not only for the variable, but also for all of its parts.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])
hadMember(d, list0)
hadMember(d, list1)
hadMember(d, list2)

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g6, u7)
```

[![PROV mapping for assignments of list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/list_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent dictionaries.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="script:name"])

hadMember(x, list0)
hadMember(x, list1)
hadMember(x, list2)

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g7, u8)
```

[![PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/list_assign2.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/list_assign2.pdf)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return.

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d, [value="3", type="script:eval", label="len(d)"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)
```

[![PROV mapping for function call](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/call.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/call.pdf)


## Access to part of structure

We map an access as an `activity` that generates the accessed `entity`, by using the list `entity`, the list element, and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`). The generated `entity` derives from the list element.

```python
d[0]
```

```provn
entity(0, [value="0", type="script:literal"])
entity(d_ac0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d_ac0, list0, access1, g8, u9)
```

[![PROV mapping for accesses to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/access.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/access.pdf)


## Assignment to part of structure

A part assignment is similitar to an assignment, but it creates a new `entity` for the whole `entity` with `hadMember` relationships to the new part and to the other parts that are valid.

If there is more than one variable or data structure with a reference to the changed list, we must update all the lists.

The assignment `activity` uses all the changed `entities` and generates new versions of them. Additionally, it uses the right side of the assignment to derive an entity for the left side.

```python
d[1] = 3
```

```provn
entity(3, [value="3", type="script:literal"])
entity(list1#2, [value="3", type="script:access", label="d[1]"])

activity(assign4, [type="script:assign"])
used(assign4, 1, -)
wasDerivedFrom(list1#2, 3, assign4, g9, u10)

entity(d#2, [value="[10000, 3, 10000]", type="script:name", label="d"])
wasDerivedFrom(d#2, d, assign4, g10, u11)
wasDerivedFrom(d#2, 3, assign4, g10, u10)
hadMember(d#2, list0)
hadMember(d#2, list1#2)
hadMember(d#2, list2)

entity(x#2, [value="[10000, 3, 10000]", type="script:name", label="x"])
wasDerivedFrom(x#2, x, assign4, g11, u12)
wasDerivedFrom(x#2, 3, assign4, g11, u10)
hadMember(x#2, list0)
hadMember(x#2, list1#2)
hadMember(x#2, list2)
```

[![PROV mapping for assignments to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/part_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/part_assign.pdf)


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
    
// assignment
entity(10000, [value="10000", type="script:literal"])
entity(m, [value="10000", type="script:name", label="m"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1)

// operation
entity(1, [value="1", type="script:literal"])
entity(sum, [value="10001", type="script:sum", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)

// list definition
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]"])
entity(list0, [value="10000", type="script:item", label="m"])
entity(list1, [value="10001", type="script:item", label="m + 1"])
entity(list2, [value="10000", type="script:item", label="m"])

hadMember(list, list0)
hadMember(list, list1)
hadMember(list, list2)

activity(definelist1, [type="script:definelist"])
wasDerivedFrom(list0, m, definelist1, g3, u4)
wasDerivedFrom(list1, sum, definelist1, g4, u5)
wasDerivedFrom(list2, m, definelist1, g5, u6)
wasGeneratedBy(list, definelist1, -)

// list assignment
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d"])
hadMember(d, list0)
hadMember(d, list1)
hadMember(d, list2)

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g6, u7)


// list assignment 2
entity(x, [value="[10000, 10001, 10000]", type="script:name"])

hadMember(x, list0)
hadMember(x, list1)
hadMember(x, list2)

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g7, u8)

// call
entity(len_d, [value="3", type="script:eval", label="len(d)"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="script:literal"])
entity(d_ac0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d_ac0, list0, access1, g8, u9)

// part assignment
entity(3, [value="3", type="script:literal"])
entity(list1#2, [value="3", type="script:access", label="d[1]"])

activity(assign4, [type="script:assign"])
used(assign4, 1, -)
wasDerivedFrom(list1#2, 3, assign4, g9, u10)

entity(d#2, [value="[10000, 3, 10000]", type="script:name", label="d"])
wasDerivedFrom(d#2, d, assign4, g10, u11)
wasDerivedFrom(d#2, 3, assign4, g10, u10)
hadMember(d#2, list0)
hadMember(d#2, list1#2)
hadMember(d#2, list2)

entity(x#2, [value="[10000, 3, 10000]", type="script:name", label="x"])
wasDerivedFrom(x#2, x, assign4, g11, u12)
wasDerivedFrom(x#2, 3, assign4, g11, u10)
hadMember(x#2, list0)
hadMember(x#2, list1#2)
hadMember(x#2, list2)
```

[![PROV mapping](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/full.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/full.pdf)