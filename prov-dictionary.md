# PROV-Dictionary

In this document we map simple script constructs to PROV-Dictionary.

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
entity(True, [value="True", type="script:constant"])
entity(int, [value="<class 'int'>", type="script:name", label="int"])
entity(ellipsis, [value="Ellipsis", type="script:constant", label="..."])
```

[![PROV-Dictionary mapping for names, literals, and constants](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/names.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/names.pdf)

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

[![PROV-Dictionary mapping for assignments](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/assign.pdf)

## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

```python
m + 1
```

```provn
entity(1, [value="1", type="script:literal"])
entity(sum, [value="10001", type="eval", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)
```

[![PROV-Dictionary mapping for operations](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/operation.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/operation.pdf)

## List definition

A list is represented by a PROV-Dictionary that has the list indexes as keys.

According to the [PROV-Dictionary documentation](https://www.w3.org/TR/prov-dictionary/), a complete dictionary must be able to be traced back to an empty dictionary. Since we have the complete list definition, we always define a list entity by creating an empty dictionary. Then, we use the `derivedByInsertionFrom` relationship to insert its elements.

The provenance of a `Floyd-Warshall` execution should indicate the position of accessed elements in the result matrix (list of lists) to allow the querying of the shortest-path between two nodes. However, the PROV-Dictionary extension does not indicate accesses to positions (note below that an `entity` may repeat in multiple positions). Thus, to allow this query, we create an extra `entity` for every position in the list and we use an `activity` to derive these `entities` from the actual `entities` that compose the dictionary.

For simplicity, in the case of the definition of matrices, we use a single `activity` to represent all the derivations, instead of an `activity` for each row.

```python
[m, m + 1, m]
```

```provn
entity(empty, [value="[]", type="EmptyDictionary"])
entity(list, [value="[10000, 10001, 10000]", type="Dictionary", label="[m, m + 1, m]"])
entity(list0, [value="10000", type="script:item", label="m"])
entity(list1, [value="10001", type="script:item", label="m + 1"])
entity(list2, [value="10000", type="script:item", label="m"])
derivedByInsertionFrom(
    list, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(definelist1, [type="script:definelist"])
wasDerivedFrom(list0, m, definelist1, g3, u4)
wasDerivedFrom(list1, sum, definelist1, g4, u5)
wasDerivedFrom(list2, m, definelist1, g5, u6)
wasGeneratedBy(list, definelist1, -)
```

[![PROV-Dictionary mapping for list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/list.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/list.pdf)


# Assignment of list definition

When we assign a list definition to a variable, the variable is also a dictionary. The PROV-Dictionary extension does not have a derivation rule to indicate that a dictionary is the same as the other. Thus, we must create a new dictionary that have the same keys as the existing one.

Note that we do not create new entities for the dictionary members. We just reuse the existing ones. Note however that we create an empty dictionary and derive the new one from it.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="Dictionary", label="d"])
derivedByInsertionFrom(
    d, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g6, u7)
```

[![PROV-Dictionary mapping for assignments of list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/list_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/list_assign.pdf)

The same mapping is valid for assignments to names that represent dictionaries.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="Dictionary", label="x"])
derivedByInsertionFrom(
    x, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g7, u8)
```

[![PROV-Dictionary mapping for assignments to names that have list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/list_assign2.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/list_assign2.pdf)


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

[![PROV-Dictionary mapping for function call](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/call.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/call.pdf)

## Access to part of structure

We map an access as an `activity` that generates the accessed `entity`, by using the list `entity`, the list element, and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`). The generated `entity` derives from the list element.

```python
d[0]
```

```provn
entity(0, [value="0", type="script:literal"])
entity(d@0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d@0, list0, access1, g8, u9)
```

[![PROV-Dictionary mapping for accesses to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/access.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/access.pdf)

## Assignment to part of structure

A part assignment is similitar to an assignment, but it produces a dictionary derivation using `derivedByInsertionFrom`.

If there is more than one variable or data structure with a reference to the changed list, we must update all the lists.

The assignment `activity` uses all the changed `entities` and generates new versions of them. Additionally, it uses the right side of the assignment to derive an entity for the left side.

```python
d[1] = 3
```

```provn
entity(3, [value="3", type="script:literal"])

entity(d@1, [value="3", type="script:access"])
activity(assign4, [type="script:assign"])
used(assign4, 1, -)
wasDerivedFrom(d@1, 3, assign4, g9, u10)

entity(d#2, [value="[10000, 3, 10000]", type="Dictionary", label="d"])
wasDerivedFrom(d#2, d, assign4, g10, u11)
wasDerivedFrom(d#2, 3, assign4, g10, u10)
derivedByInsertionFrom(d#2, d, {("1", d@1)})

entity(x#2, [value="[10000, 3, 10000]", type="Dictionary", label="x"])
wasDerivedFrom(x#2, x, assign4, g11, u12)
wasDerivedFrom(x#2, 3, assign4, g11, u10)
derivedByInsertionFrom(x#2, x, {("1", d@1)})
```

[![PROV-Dictionary mapping for assignments to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/part_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/part_assign.pdf)

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
entity(sum, [value="10001", type="eval", label="m + 1"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)

// list definition
entity(empty, [value="[]", type="EmptyDictionary"])
entity(list, [value="[10000, 10001, 10000]", type="Dictionary", label="[m, m + 1, m]"])
entity(list0, [value="10000", type="script:item", label="m"])
entity(list1, [value="10001", type="script:item", label="m + 1"])
entity(list2, [value="10000", type="script:item", label="m"])
derivedByInsertionFrom(
    list, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(definelist1, [type="script:definelist"])
wasDerivedFrom(list0, m, definelist1, g3, u4)
wasDerivedFrom(list1, sum, definelist1, g4, u5)
wasDerivedFrom(list2, m, definelist1, g5, u6)
wasGeneratedBy(list, definelist1, -)

// list assignment
entity(d, [value="[10000, 10001, 10000]", type="Dictionary", label="d"])
derivedByInsertionFrom(
    d, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g6, u7)

// list assignment 2
entity(x, [value="[10000, 10001, 10000]", type="Dictionary", label="x"])
derivedByInsertionFrom(
    x, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g7, u8)

// call
entity(len_d, [value="3", type="script:eval", label="len(d)"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="script:literal"])
entity(d@0, [value="10000", type="script:access", label="d[0]"])

activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d@0, list0, access1, g8, u9)

// part assignment
entity(3, [value="3", type="script:literal"])

entity(d@1, [value="3", type="script:access"])
activity(assign4, [type="script:assign"])
used(assign4, 1, -)
wasDerivedFrom(d@1, 3, assign4, g9, u10)

entity(d#2, [value="[10000, 3, 10000]", type="Dictionary", label="d"])
wasDerivedFrom(d#2, d, assign4, g10, u11)
wasDerivedFrom(d#2, 3, assign4, g10, u10)
derivedByInsertionFrom(d#2, d, {("1", d@1)})

entity(x#2, [value="[10000, 3, 10000]", type="Dictionary", label="x"])
wasDerivedFrom(x#2, x, assign4, g11, u12)
wasDerivedFrom(x#2, 3, assign4, g11, u10)
derivedByInsertionFrom(x#2, x, {("1", d@1)})
```

[![PROV-Dictionary mapping](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/full.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/full.pdf)