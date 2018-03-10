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
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix version <https://dew-uff.github.io/versioned-prov/ns#>
    
entity(1, [value="1", type="script:literal", version:checkpoint="2018-02-22T16:00:00"])
entity(a, [value="'a'", type="script:literal", version:checkpoint="2018-02-22T16:00:01"])
entity(a#2, [value="b'a'", type="script:literal", version:checkpoint="2018-02-22T16:00:02"])
entity(True, [value="True", type="script:constant", version:checkpoint="2018-02-22T16:00:03"])
entity(int, [value="<class 'int'>", type="script:name", label="int", version:checkpoint="2018-02-22T16:00:04"])
entity(ellipsis, [value="Ellipsis", type="script:constant", label="...", version:checkpoint="2018-02-22T16:00:05"])
```

[![Versioned-PROV mapping for names, literals, and constants](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/names.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/names.pdf)


## Assignment

We map assignments as `activities`. A variable assignment always generates a new entity, even when the previous name already exists. This is important to distinguish the version used by each entity in a given time.

If the element on the left side of the assignment references the same value as the element on the right, we use the `referenceDerivedFrom` relationship instead of the `wasDerivedFrom`.

This relationship indicates the time of derivation and allows us to get the version of the new entity by navigating from the left side entity to the right side entity.

```python
m = 10000
```

```provn
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix version <https://dew-uff.github.io/versioned-prov/ns#>
    
entity(10000, [value="10000", type="script:literal", version:checkpoint="1"])
entity(m, [value="10000", type="script:name", label="m", version:checkpoint="2"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="version:Reference", version:checkpoint="2"])
```

[![Versioned-PROV mapping for assignments](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/assign.pdf)


## Operation

Similar to assigments, we also use `activities` to map operations. However, instead of producing an `entity` for a variable name, it produces an `entity` for the evaluation result.

If the operation produces a different value from its operands, we use the `wasDerivedFrom` relationship. Otherwise, we use the `referenceDerivedFrom` relationship.

```python
m + 1
```

```provn
entity(1, [value="1", type="script:literal",  version:checkpoint="3"])
entity(sum, [value="10001", type="script:eval", label="m + 1", version:checkpoint="4"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)
```

[![Versioned-PROV mapping for operations](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/operation.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/operation.pdf)


## List definition

A list is defined by the `derivedByInsertion` relationship. This relationship indicates which items a list has at a given time.

```python
[m, m + 1, m]
```

```provn
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]", version:checkpoint="5"])
hadMember(list, m, [type="version:Insertion", version:key="0", version:checkpoint="5"])
hadMember(list, sum, [type="version:Insertion", version:key="1", version:checkpoint="5"])
hadMember(list, m, [type="version:Insertion", version:key="2", version:checkpoint="5"])
```

[![Versioned-PROV mapping for list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list.pdf)


Comparison:

* In this mapping, accesses to parts indicate the positions of accesses. Thus, we do not need to create additional entities or activities to answer the provenance query of Floyd-Warshall.



## Assignment of list definition

In this mapping, the assignment of a list is exactly the same as any other assignment. Thus, we just use the `referenceDerivedFrom` relationship to indicate that the entity share a reference.

```python
d = [m, m + 1, m]
```

```provn
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d", version:checkpoint="6"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="version:Reference", version:checkpoint="6"])
```

[![Versioned-PROV mapping for assignments of list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list_assign.pdf)

The same mapping is valid for assignments to names that represent lists.

```python
x = d
```

```provn
entity(x, [value="[10000, 10001, 10000]", type="name", label="x", version:checkpoint="7"])

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="version:Reference", version:checkpoint="7"])
```

[![Versioned-PROV mapping for assignments to names that have list definitions](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/list_assign2.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/list_assign2.pdf)


## Function call

We map a function call as an `activity` that `uses` its parameters and `generates` an `entity` with its return.

When we do not know the function call implementation, we cannot use `derivation` relationships.

```python
len(d)
```

```provn
entity(len_d, [value="3", type="script:eval", label="len(d)", version:checkpoint="8"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)
```

[![Versioned-PROV mapping for function call](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/call.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/call.pdf)


## Access to part of structure

We map an access to a part of a value as an `activity` that generates the accessed `entity`, by using the list `entity` and the index, when it is explicitly used (for-each loops iterates over lists without explicit item `entities`).

We also use the `referenceDerivedFromAccess` relationship to indicate which part were accessed.

```python
d[0]
```

```provn
entity(0, [value="0", type="script:literal", version:checkpoint="9"])

entity(d_ac0, [value="10000", type="script:access", label="d[0]", version:checkpoint="10"])
activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d_ac0, m, access1, g5, u6, [
    type="version:Reference", version:checkpoint="10", 
    version:whole="d", version:key="0", version:access="r"])
```

[![Versioned-PROV mapping for accesses to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/access.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/access.pdf)


## Assignment to part of structure

A part assignment is a mix of an access `activity` and an assign `activity`.

We also use the `derivedByInsertion` relationship to update a list. This relationship creates a new version based on the previous one by using the timestamp.

Additionaly, we use the `referenceDerivedFromAccess` relationship to indicate that a part of a structure was changed.


```python
d[1] = 3
```

```provn
entity(3, [value="3", type="script:literal", version:checkpoint="10"])

entity(d_ac1, [value="3", type="script:access", label="d[1]", version:checkpoint="11"])
hadMember(list, d_ac1, [type="version:Insertion", version:key="1", version:checkpoint="11"])

activity(assign4, [type="script:assign"])
used(assign4, d, -)
used(assign4, 1, -)
wasDerivedFrom(d_ac1, 3, assign4, g6, u7, [
    type="version:Reference", version:checkpoint="11",
    version:whole="d", version:key="1", version:access="w"])
```

[![Versioned-PROV mapping for assignments to parts](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/part_assign.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/part_assign.pdf)

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
prefix script <https://dew-uff.github.io/versioned-prov/ns/script#>
prefix version <https://dew-uff.github.io/versioned-prov/ns#>

// assignment
entity(10000, [value="10000", type="script:literal", version:checkpoint="1"])
entity(m, [value="10000", type="script:name", label="m", version:checkpoint="2"])

activity(assign1, [type="script:assign"])
wasDerivedFrom(m, 10000, assign1, g1, u1, [type="version:Reference", version:checkpoint="2"])

// operation
entity(1, [value="1", type="script:literal",  version:checkpoint="3"])
entity(sum, [value="10001", type="script:eval", label="m + 1", version:checkpoint="4"])

activity(+, [type="script:operation"])
wasDerivedFrom(sum, m, +, g2, u2)
wasDerivedFrom(sum, 1, +, g2, u3)

// list def
entity(list, [value="[10000, 10001, 10000]", type="script:list", label="[m, m + 1, m]", version:checkpoint="5"])
hadMember(list, m, [type="version:Insertion", version:key="0", version:checkpoint="5"])
hadMember(list, sum, [type="version:Insertion", version:key="1", version:checkpoint="5"])
hadMember(list, m, [type="version:Insertion", version:key="2", version:checkpoint="5"])

// list assign
entity(d, [value="[10000, 10001, 10000]", type="script:name", label="d", version:checkpoint="6"])

activity(assign2, [type="script:assign"])
wasDerivedFrom(d, list, assign2, g3, u4, [type="version:Reference", version:checkpoint="6"])

// list assign x
entity(x, [value="[10000, 10001, 10000]", type="name", label="x", version:checkpoint="7"])

activity(assign3, [type="script:assign"])
wasDerivedFrom(x, d, assign3, g4, u5, [type="version:Reference", version:checkpoint="7"])

// call
entity(len_d, [value="3", type="script:eval", label="len(d)", version:checkpoint="8"])

activity(call1, [type="script:call", label="len"])
used(call1, d, -)
wasGeneratedBy(len_d, call1, -)

// part access
entity(0, [value="0", type="script:literal", version:checkpoint="9"])

entity(d_ac0, [value="10000", type="script:access", label="d[0]", version:checkpoint="10"])
activity(access1, [type="script:access"])
used(access1, d, -)
used(access1, 0, -)
wasDerivedFrom(d_ac0, m, access1, g5, u6, [
    type="version:Reference", version:checkpoint="10", 
    version:whole="d", version:key="0", version:access="r"])

// part assign
entity(3, [value="3", type="script:literal", version:checkpoint="10"])

entity(d_ac1, [value="3", type="script:access", label="d[1]", version:checkpoint="11"])
hadMember(list, d_ac1, [type="version:Insertion", version:key="1", version:checkpoint="11"])

activity(assign4, [type="script:assign"])
used(assign4, d, -)
used(assign4, 1, -)
wasDerivedFrom(d_ac1, 3, assign4, g6, u7, [
    type="version:Reference", version:checkpoint="11",
    version:whole="d", version:key="1", version:access="w"])
```

[![Versioned-PROV mapping](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/full.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/full.pdf)