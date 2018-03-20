::SET BASE = generated::

# Comparison

In this document, we compare PROV, PROV-Dictionary and Versioned-PROV. We divide our comparison into `nodes` that represent key PROV concepts (e.g., `entity`, `activity`, ...), and `edges` that represent all other PROV-N statements (e.g., `wasDerivedFrom`, `wasGeneratedBy`, ...).


## List Definition

For the list `[1, 2, 1]`, we have 2 entities to represent the literals `1` and `2` in all mappings:
```
entity(1, [value="1", type="name"])
entity(2, [value="2", type="name"])
```


Besides these 2 entities, all mappings have an entity to represent the list definition itself, but the `type` attribute of the mappings change. In PROV and Versioned-PROV, the `type` must be a `prov:Collection`. In PROV-Dictionary, the `type` must be a `prov:Dictionary`. Note that all entity types that we use in the `script` namespace that we use in the examples (except `script:literal`, and `script:constant`) are subtype of `prov:Collection`, even when they do not represent collections.
```
entity(list, [value="[1, 2, 1]", type="X", label="[1, 2, 1]"])
```

The Plain PROV mapping use the `hadMember` statement to define members of the list. This statement does not indicate the position of the elements in the list. Since this information is important to reconstruct the path in the provenance query of Floyd-Warshall, we create extra nodes that encode the list position and we derive theses nodes from the original literal entities, by using the `definelist` activity:
```
activity(definelist1, [type="script:definelist"])
wasGeneratedBy(list, definelist1, -)

entity(list0, [value="1", type="script:item", label="1"])
hadMember(list, list0)
wasDerivedFrom(list0, 1, definelist1, g1, u1)

entity(list1, [value="1", type="script:item", label="2"])
hadMember(list, list1)
wasDerivedFrom(list1, 2, definelist1, g2, u2)

entity(list2, [value="2", type="script:item", label="1"])
hadMember(list, list2)
wasDerivedFrom(list2, 1, definelist1, g3, u3)
```


Different from Plain PROV, PROV-Dictionary can define list elements with their positions, and can use a single statement, `derivedByInsertionFrom`, to associate member entities to a collection entity. However, since it does not indicate the position of accesses, we still need to create extra entities to encode the position. Additionally, we also need a global `EmptyDictionary` entity for the derivation:
```
entity(empty, [value="[]", type="EmptyDictionary"])

activity(definelist1, [type="script:definelist"])
wasGeneratedBy(list, definelist1, -)

entity(list0, [value="1", type="script:item", label="1"])
wasDerivedFrom(list0, 1, definelist1, g1, u1)

entity(list1, [value="1", type="script:item", label="2"])
wasDerivedFrom(list1, 2, definelist1, g2, u2)

entity(list2, [value="2", type="script:item", label="1"])
wasDerivedFrom(list2, 1, definelist1, g3, u3)

derivedByInsertionFrom(
    list, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)
```

Versioned-PROV is capable of defining list elements with their positions using the `hadMember` statement with extra attributes, and it also indicates the accessed positions. Thus, Versioned-PROV queries can handle list accesses without requiring extra constructs:
```
hadMember(list, 1, [type="version:Put", version:key="0", version:checkpoint="1"])
hadMember(list, 2, [type="version:Put", version:key="1", version:checkpoint="1"])
hadMember(list, 1, [type="version:Put", version:key="2", version:checkpoint="1"])
```

In the following table, we count how many statements of each kind, each approach requires for defining a list with N elements. Note that we are not counting the statements that appear in the list, since they can be defined prior to the list definition.

Statement               | Common | PROV     | PROV-Dictionary | Versioned-PROV |
:-----------------------|:------:|:--------:|:---------------:|:--------------:|
`entity`                |1       |N         |N + 1ᴳ           |                |
`activity`              |        |1         |1                |                |
**Nodes**               |**1**   |**N + 1** |**N + 1 + 1ᴳ**   |**0**           |
=====================   |=====   |======    |===========      |=====           |
`wasDerivedFrom`        |        |N         |N                |                |
`wasGeneratedBy`        |        |1         |1                |                |
`hadMember`             |        |N         |                 |N               |
`derivedByInsertionFrom`|        |          |1                |                |
**Edges**               |**0**   |**2N + 1**|**N + 2**        |**N**           |
=====================   |=====   |======    |===========      |=====           |
**Total**               |**1**   |**3N + 2**|**2N + 3 + 1ᴳ**  |**N**           |

ᴳ Global EmptyDictionary entity that appears only once.


::![Graph](::GET BASE::/comparison/list)

## Reference assignment

Common assignments of imutable values produce the same number of elements in all the mappings. However, the assignment of references to data structures requires recreating the membership relationships in Plain PROV and PROV-Dictionary.

In all mappings, we have the following statements to represent `d = [1, 2, 1]`:
```
entity(d, [value="[1, 2, 3]", type="script:name", label="d"])
activity(assign1, [type="script:assign"])
wasDerivedFrom(d, list, assign1, ga1, ua1, [type="version:Reference", version:checkpoint="2"])
```
Once again, the attributes in the version namespace refer to the Versioned-PROV mapping.


The Plain PROV mapping uses `hadMember` relationships to define the memberships:
```
hadMember(d, list0)
hadMember(d, list1)
hadMember(d, list2)
```
Thus, we use N statements for a list of N elements

The PROV-Dictionary mapping uses a single `derivedByInsertionFrom` to define the memberships:
```
derivedByInsertionFrom(
    d, empty,
    {("0", list0), ("1", list1), ("2", list2)}
)
```

Finally, the Versioned-PROV mapping does not require any additional constructs other than the attributes in `wasDerivedFrom`. Hence assignments of imutable or mutable values in Versioned-PROV are represented the same way.


In the following table, we count how many statements of each kind, each approach requires for assigning a reference to a list with N elements.

Statement               | Common | PROV     | PROV-Dictionary | Versioned-PROV |
:-----------------------|:------:|:--------:|:---------------:|:--------------:|
`entity`                |1       |          |                 |                |
`activity`              |1       |          |                 |                |
**Nodes**               |**2**   |**0**     |**0**            |**0**           |
=====================   |=====   |======    |===========      |=====           |
`wasDerivedFrom`        |1       |          |                 |                |
`hadMember`             |        |N         |                 |                |
`derivedByInsertionFrom`|        |          |1                |                |
**Edges**               |**1**   |**N**     |**1**            |**0**           |
=====================   |=====   |======    |===========      |=====           |
**Total**               |**3**   |**N**     |**1**            |**0**           |

::![Graph](::GET BASE::/comparison/assign)

## Assignment to part of structures

An assignment to a part of a structure is similar to an assignment, but it has to update that membership of the structure. In all mappings, to represent `d[1] = 3` we have the following statements in common:
```
entity(3, [value="3", type="name", version:checkpoint="5"])

entity(d_ac1, [value="3", type="script:access", label="d[1]"])
activity(assign2, [type="script:assign"])
used(assign2, 1, -)
wasDerivedFrom(d_ac1, 3, assign2, ga2, ua2, [
    type="version:Reference", version:checkpoint="3",
    version:whole="d", version:key="1", version:access="w"])
```
Once again, the attributes in the version namespace refer to the Versioned-PROV mapping.

This snippet deals with the generation of the new member entity, but it does not deal with the update of the collection entity. The update on the collection entity should occur not only on the collection being updated, but also to all collections that share its reference.
Each mapping tackles this update differently.

Plain PROV has no semantics to update the membership of an entity. Thus, it is necessary to create a new `entity` for every collection that reference the same data structures and redefine its structure:
```
entity(d#2, [value="[1, 3, 1]", type="script:name", label="d"])
wasDerivedFrom(d#2, d, assign2, ga3, ua3)
wasDerivedFrom(d#2, 3, assign2, ga3, ua2)
hadMember(d#2, list0)
hadMember(d#2, d_ac1)
hadMember(d#2, list2)

entity(list#2, [value="[1, 3, 1]", type="script:list"])
wasDerivedFrom(list#2, list, assign2, ga4, ua4)
wasDerivedFrom(list#2, 3, assign2, ga4, ua2)
hadMember(list#2, list0)
hadMember(list#2, d_ac1)
hadMember(list#2, list2)
```


PROV-Dictionary can use the `derivedByInsertionFrom` statement to derive new collections based on existing ones. Thus, the number of constructs is smaller:
```
entity(d#2, [value="[1, 3, 1]", type="Dictionary", label="d"])
wasDerivedFrom(d#2, d, assign2, ga3, ua3)
wasDerivedFrom(d#2, 3, assign2, ga3, ua2)
derivedByInsertionFrom(d#2, d, {("1", d_ac1)})

entity(list#2, [value="[1, 3, 1]", type="Dictionary"])
wasDerivedFrom(list#2, list, assign2, ga4, ua4)
wasDerivedFrom(list#2, 3, assign2, ga4, ua2)
derivedByInsertionFrom(list#2, list, {("1", d_ac1)})
```

Finally, in Versioned-PROV we use the `hadMember` on the collection that defined the reference and a timestamp to indicate when it became a valid member of the collection. All references that share the reference do not need to be updated, since we can follow the references using the `type="version:Reference"` in `wasDerivedFrom` statements:
```
used(assign2, d, -)
hadMember(list, d_ac1, [type="version:Put", version:key="1", version:checkpoint="3"])
```

In the following table, we count how many statements of each kind, each approach requires for assigning a element to a collection that share R references and N elements. Note that we are not counting the entities that represent the collection itself, the entity that represents the key nor the entity that represents the assigned value.

Statement               | Common | PROV         | PROV-Dictionary | Versioned-PROV |
:-----------------------|:------:|:------------:|:---------------:|:--------------:|
`entity`                |1       |R             |R                |                |
`activity`              |1       |              |                 |                |
**Nodes**               |**2**   |**R**         |**R**            |**0**           |
=====================   |=====   |=========     |=======          |=====           |
`wasDerivedFrom`        |1       |2R            |2R               |                |
`used`                  |1       |              |                 |1               |
`hadMember`             |        |R * N         |                 |1               |
`derivedByInsertionFrom`|        |              |R                |                |
**Edges**               |**2**   |**R * N + 2R**|**3R**           |**2**           |
=====================   |=====   |=========     |=======          |=====           |
**Total**               |**4**   |**R * N + 3R**|**4R**           |**2**           |


The number of statements in PROV and PROV-Dictionary are lower bounds, however. If `d` or `list` were a member of another collection, we would have to update the parent collection in a similar way. Additionally, if the entity on the right side were an assignment, we would have to update the membership of `d_ac1` as described before. The same does not happen for Versioned-PROV due to the derivation `type="version:Reference"`. Hence, for Versioned-PROV this number is at the same time the lower bound and the upper bound of an assignment in the format `COLLECTION[KEY] = VALUE`.


* In this example, we update the entity `list` as it also refers to `d`, but in an actual execution, the `list` reference is not valid anymore at this point of the execution, since it represents only the list definition. However, all other variables that share a reference with `d` would still be updated this way.

::![Graph](::GET BASE::/comparison/part)