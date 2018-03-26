::SET BASE = generated::
::SET NAME = Versioned-PROV::
::SET PLAIN_PROV = Plain PROV::
::SET PROV_DICTIONARY = PROV-Dictionary::
::SET MUTABLE_PROV = Mutable-PROV::
::SET INTERTWINED_PROV = Intertwined-PROV::
::SET VERSIONED_PROV = Versioned-PROV::


# ::GET NAME::

::GET NAME:: is a PROV extension that adds support for the provenance of mutable values by time-versioning entities. This extension is useful to represent fine-grained provenance from scripts with multiple variables refering to the same data structures and nested data-structures.


PROV does not properly support fine-grained provenance with mutable data structures due the assumption of immutable entities and their representation may become quite verbose. The PROV-Dictionary extension intends to provide data structures support for PROV, but it stills fails to accomodate the mutability of them. In this repository, we propose a new extension to support the representation of mutable data structures in PROV: ::GET VERSIONED_PROV::


*::GET PLAIN_PROV::* suffers from two main problems: (P1) when an entity that represents a collection is changed (e.g., a list is updated to add an element), a new entity should be created, together with multiple new relationships, connecting the new entity to each of the existing or new entities that represent the elements of the collection; and (P2) when more than one variable is assigned to the same collection, and one of the variables changes, all other variables should also change, as they refer to the same memory area. This means that a new entity should be created for each variable that contains the collection, together with edges for all entities that represent the elements of the collection. These problems lead to O(N) and Ω(R×N) extra elements in the provenance graph, respectively, for collections with N elements and R references.


The *::GET PROV_DICTIONARY::* extension [9] improves the support for data structures in PROV by adding derivation statements that indicate that a new collection shares most elements of the old one, but with the insertion or removal of specific elements. This solves problem P1 since it reduces the number of edges to 1. However, it still suffers from problem P2, since it still requires updating all entities that refer to the same collection when it changes. Thus, it leads to Ω(R) extra elements.


*::GET VERSIONED_PROV::* is an extension that adds reference sharing and checkpoints to PROV. Checkpoints solve problem P1 by allowing the representation of multiple versions of collections with a single entity. Reference sharing solves problem P2 by allowing collections to be represented only once and referred to by other entities through reference derivations together with checkpoints to indicate states. *::GET VERSIONED_PROV::* solves both problems in O(1).


## Running Example

To describe and evaluate the extension, we use the ::[Floyd-Warshall](algorithm.py) algorithm. This algorithm calculates the distance of the shortest path between all pairs of nodes in a weighted graph.

By running the Floyd-Warshall in the graph below, and reading the distance between the nodes 0 and 2, it should output 3. By looking at graph, we can see that this path goes from node 0 to node 1 to node 2, instead of using the direct path from node 0 to node 2. However, the Floyd-Warshall algorithm only calculates the distance, and not the paths.

::![Graph](::GET BASE::/graphs/graph)

Due the nature of the algorithm, fine-grained provenance can assist in obtained the path. In Floyd-Warshall, considering the nodes `x`, `y`, and `z`, if the sum of the sub-paths `x -> y` and `y -> z` is smaller than the sum of the path `x -> z`, then it updates the value of the path `x -> z` by the sum. Thus, the provenance of the updated `x -> z` should indicate that it was composed by the sum of `x -> y` and `y -> z`.

## Experiment

For our experiment, we collected the provenance of Floyd-Warshall algorithm and mapped it to ::GET PLAIN_PROV::, ::GET PROV_DICTIONARY::, and ::GET VERSIONED_PROV::. For descriptions of the mappings, please refer to:
  - [::GET PLAIN_PROV:: Mapping](prov.html)
  - [::GET PROV_DICTIONARY:: Mapping](prov-dictionary.html)
  - [::GET VERSIONED_PROV:: Mapping](versioned-prov.html)

We tried to produce the minimum set of PROV-N statements in the mappings without compromising the semantics. For this reason, we use the [Inference 11](https://www.w3.org/TR/prov-constraints/#derivation-generation-use-inference) to avoid using `used` and `wasGeneratedBy` statements when we have `wasDerivedFrom` statements.


The ::GET PLAIN_PROV:: mapping produced the following graph:

::![Floyd-Warshall in ::GET PLAIN_PROV::](::GET BASE::/plain_prov/floydwarshall)
::[Click here for an organized version](::GET BASE::/plain_prov/floydwarshall_org.pdf)

The ::GET PROV_DICTIONARY:: mapping produced the following graph:

::![Floyd-Warshall in ::GET PROV_DICTIONARY::](::GET BASE::/prov_dictionary/floydwarshall)
::[Click here for an organized version](::GET BASE::/prov_dictionary/floydwarshall_org.pdf)

The ::GET VERSIONED_PROV:: mapping produced the following graph:

::![Floyd-Warshall in ::GET VERSIONED_PROV::](::GET BASE::/versioned_prov/floydwarshall)
::[Click here for an organized version](::GET BASE::/versioned_prov/floydwarshall_org.pdf)

The following table presents the count of each node (entity, activity, value) and relationship (wasDerivedFrom, used, ...) definition in each approach.

::LOAD(::GET BASE::/table.md)


The figure below compares the number of nodes (i.e., `entity`, `activity`, ...) and relationships (i.e., `wasDerivedFrom`, `used`, `wasGeneratedBy`, ...) of each approach. ::GET VERSIONED_PROV:: is the approach with less componenens. In ::GET VERSIONED_PROV::, the `hadMember` relationship with a `checkpoint` indicates the creation of a new version for the entity. Thus, it replaces some entities that exist in the other approaches by this relationship. However, the other approaches also require similar relationships to indicate the membership of elements in data structures. Hence, this replacement does not result in a bigger number of relationships. Additionally, all the other attributes of this approach appear in existing statements of the other approaches. So, the addition of the attributes do not increase the number of components.


::![Comparison of elements](::GET BASE::/graphs/paper_comparison)


The ::GET PROV_DICTIONARY:: approach creates a new `entity` when there is a change on an existing `entity` and when there is an access to an `entity` that represents a data-structure. Thus, it presents more nodes and relationships than ::GET VERSIONED_PROV::. However, it presents less relationships than the ::GET PLAIN_PROV:: approach. This occurs because, the ::GET PLAIN_PROV:: also creates new `entities` on changes, but has no mechanisms to indicate that an `entity` has all members of the previously existing `entity`, thus it requires many `hadMember` relationship for every `entity` that represent data structures. The number of nodes in ::GET PLAIN_PROV:: and ::GET PROV_DICTIONARY:: could be equivalent, however, according to the ::GET PROV_DICTIONARY:: specification, for a dictionary to be deterministic, its derivation chain should end in an `EmptyDictionary` `entity`. Hence, we need one extra node for the ::GET PROV_DICTIONARY:: approach.


The following figure considers only the nodes and edges overheads related to list definitions, reference derivations, and part assignments. These are the only operations that differ in these three approaches. Note that ::GET VERSIONED_PROV:: has no node overhead. This occurs because it does not require the creation of new entities when a collection changes.


::![Comparison of elements](::GET BASE::/graphs/specific_comparison)


For an in depth analaysis of space requirements of these approaches, please take a a look at our [Comparison](comparison.html).


## Query

As stated before, the access `result[0][2]` represents de distance of the shortest path between the node 0 and the node 2 in the graph. This access is represented by the entity `result@0@2` in our mappings.
The provenance query of this entity should indicate which other parts of the graph were used to construct the shortest path, thus indicating the path. The following figures present the query result in each mapping.

The ::GET PLAIN_PROV:: mapping produces the following query result:

::![Query in ::GET PLAIN_PROV::](::GET BASE::/plain_prov/query)

The ::GET PROV_DICTIONARY:: mapping produces the following query result:

::![Query in ::GET PROV_DICTIONARY::](::GET BASE::/prov_dictionary/query)


The ::GET VERSIONED_PROV:: mapping produces the following query result:

::![Query in ::GET VERSIONED_PROV::](::GET BASE::/versioned_prov/query)

Querying with ::GET VERSIONED_PROV:: is harder than querying with ::GET PLAIN_PROV::, and ::GET PROV_DICTIONARY::, since the former mapping may include cycles and requires navigating through different edges. However, these mappings allow better derivation queries, by identifing that an entity that was generated as a part of a data structure was derived from the data structure, without deriving from the other parts of the data structure. Due the lack of support for this kind of derivation in ::GET PLAIN_PROV:: and ::GET PROV_DICTIONARY::, we opted to omit membership derivations in the first two figures of this section.

## Namespaces

In this repository we use two namespaces:

* We use the namespace [`version:`](ns) for general ::GET VERSIONED_PROV:: concepts
* On the other hand, the namespace [`script:`](ns/script) indicates specific script concepts for our FLoyd-Warshall mapping.

## Authors

- João Felipe Pimentel (Universidade Federal Fluminense)
- Paolo Missier (Newcastle University)
- Leonardo Murta (Universidade Federal Fluminense)
- Vanessa Braganholo (Universidade Federal Fluminense)
