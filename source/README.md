::SET BASE = generated::
::SET NAME = Versioned-PROV::
::SET PLAIN_PROV = Plain PROV::
::SET PROV_DICTIONARY = PROV-Dictionary::
::SET MUTABLE_PROV = Mutable-PROV::
::SET INTERTWINED_PROV = Intertwined-PROV::
::SET VERSIONED_PROV = Versioned-PROV::


# ::GET NAME::

::GET NAME:: is a PROV extension that adds support for the provenance of mutable values through the timed-versioning of entities. This extension is useful to represent fine-grained provenance from scripts with multiple variables refering to the same data structures and nested data-structures.


PROV does not properly support fine-grained provenance with mutable data structures due the assumption of immutable entities and their representation may become quite verbose. The PROV-Dictionary extension intends to provide data structures support for PROV, but it stills fails to accomodate the mutability of them. In this repository, we propose a new extensions to support the representation of mutable data structures in PROV: ::GET VERSIONED_PROV::


*::GET PLAIN_PROV::* suffers from two main problems: (P1) when a collection entity is changed, a new collection entity should be created, together with multiple new edges, connecting the new collection entity to the existing or new part entities; and (P2) when more than one variable is assigned to the same collection, and one of the variables changes, all other variables should also change, as they refer to the same memory area, meaning that a new entity should be created for each variable that contains the collection, together with edges for all part entities. Both problems lead to having many extra edges and nodes in the provenance graph.

*::GET PROV_DICTIONARY::* solves the problem P1, but stil sufers from the problem P2.

*::GET VERSIONED_PROV::* solves these problems using a fine-grained versioning strategy.


## Running Example

To describe and evaluate the extension, we use the ::[Floyd-Warshall](algorithm.py) algorithm. This algorithm calculates the distance of the shortest path between all pairs of nodes in a weighted graph.

By running the Floyd-Warshall in the graph below, and reading the distance between the nodes 0 and 2, it should output 3. By looking at graph, we can see that this path goes from node 0 to node 1 to node 2, instead of using the direct path from node 0 to node 2. However, the Floyd-Warshall algorithm only calculates the distance, and not the paths.

::![Graph](::GET BASE::/graphs/graph)

Due the nature of the algorithm, fine-grained provenance can assist in obtained the path. In Floyd-Warshall, considering the nodes `x`, `y`, and `z`, if the sum of the sub-paths `x -> y` and `y -> z` is smaller than the sum of the path `x -> z`, then it updates the value of the path `x -> z` by the sum. Thus, the provenance of the updated `x -> z` should indicate that it was composed by the sum of `x -> y` and `y -> z`.

## Experiment

For our experiment, we collected the provenance of Floyd-Warshall algorithm and mapped it to ::GET PLAIN_PROV::, ::GET PROV_DICTIONARY::, and ::GET VERSIONED_PROV::. For descriptions of the mappings, please refer to:
  - [::GET PLAIN_PROV:: Mapping](prov.md)
  - [::GET PROV_DICTIONARY:: Mapping](prov-dictionary.md)
  - [::GET VERSIONED_PROV:: Mapping](versioned-prov.md)

We tried to produce the minimum set of PROV-N statements in the mappings without compromising the semantics. For this reason, we use the [Inference 11](https://www.w3.org/TR/prov-constraints/#derivation-generation-use-inference) to avoid using `used` and `wasGeneratedBy` statements when we have `wasDerivedFrom` statements.


The ::GET PLAIN_PROV:: mapping produced the following graph:

::![Floyd-Warshall in ::GET PLAIN_PROV::](::GET BASE::/plain_prov/floydwarshall)

The ::GET PROV_DICTIONARY:: mapping produced the following graph:

::![Floyd-Warshall in ::GET PROV_DICTIONARY::](::GET BASE::/prov_dictionary/floydwarshall)

The ::GET VERSIONED_PROV:: mapping produced the following graph:

::![Floyd-Warshall in ::GET VERSIONED_PROV::](::GET BASE::/versioned_prov/floydwarshall)

The following table presents the count of each node (entity, activity, value) and relationship (wasDerivedFrom, used, ...) definition in each approach.

::LOAD(::GET BASE::/table.md)


The figure below compares the number of nodes (i.e., `entity`, `activity`, ...) and relationships (i.e., `wasDerivedFrom`, `used`, `wasGeneratedBy`, ...) of each approach. ::GET VERSIONED_PROV:: is the approach with less componenens. In ::GET VERSIONED_PROV::, the `hadMember` relationship with a `checkpoint` indicates the creation of a new version for the entity. Thus, it replaces some entities that exist in the other approaches by this relationship. However, the other approaches also require similar relationships to indicate the membership of elements in data structures. Hence, this replacement does not result in a bigger number of relationships. Additionally, all the other attributes of this approach appear in existing statements of the other approaches. So, the addition of the attributes do not increase the number of components.


::![Comparison of elements](::GET BASE::/graphs/paper_comparison)


The ::GET PROV_DICTIONARY:: approach creates a new `entity` when there is a change on an existing `entity` and when there is an access to an `entity` that represents a data-structure. Thus, it presents more nodes and relationships than ::GET VERSIONED_PROV::. However, it presents less relationships than the ::GET PLAIN_PROV:: approach. This occurs because, the ::GET PLAIN_PROV:: also creates new `entities` on changes, but has no mechanisms to indicate that an `entity` has all members of the previously existing `entity`, thus it requires many `hadMember` relationship for every `entity` that represent data structures. The number of nodes in ::GET PLAIN_PROV:: and ::GET PROV_DICTIONARY:: could be equivalent, however, according to the ::GET PROV_DICTIONARY:: specification, for a dictionary to be deterministic, its derivation chain should end in an `EmptyDictionary` `entity`. Hence, we need one extra node for the ::GET PROV_DICTIONARY:: approach.


For an in depth analaysis of space requirements of these approaches, please take a a look at our [Comparison](comparison.md).


## Query

As stated before, the access `result[0][2]` represents de distance of the shortest path between the node 0 and the node 2 in the graph. This access is represented by the entity `result_a020` in our mappings.
The provenance query of this entity should indicate which other parts of the graph were used to construct the shortest path, thus indicating the path. The following figures present the query result in each mapping.

The ::GET PLAIN_PROV:: mapping produces the following query result:

::![Query in ::GET PLAIN_PROV::](::GET BASE::/plain_prov/query)

The ::GET PROV_DICTIONARY:: mapping produces the following query result:

::![Query in ::GET PROV_DICTIONARY::](::GET BASE::/prov_dictionary/query)


The ::GET VERSIONED_PROV:: mapping produces the following query result:

::![Query in ::GET VERSIONED_PROV::](::GET BASE::/versioned_prov/query)

Querying with ::GET VERSIONED_PROV:: is harder than querying with ::GET PLAIN_PROV::, and ::GET PROV_DICTIONARY::, since the former mapping may include cycles and requires navigating through different edges. However, these mappings allow better derivation queries, by identifing that an entity that was generated as a part of a data structure was derived from the data structure, without deriving from the other parts of the data structure. Due the lack of support for this kind of derivation in ::GET PLAIN_PROV:: and ::GET PROV_DICTIONARY::, we opted to omit membership derivations in the first two figures of this section.

## Unfold

As stated before, the ::GET VERSIONED_PROV:: mapping produces less nodes for the Floyd-Warshall algorithm and supports more meaningful queries. However, it is complete enough to be unfolded into the ::GET PLAIN_PROV:: mapping. If membership querying is not required, unfolding the ::GET VERSIONED_PROV:: mapping may be a good option to improve the performance of queries, since ::GET PLAIN_PROV:: is a DAG.


## Development

We use [Jupyter Notebooks](https://github.com/dew-uff/versioned-prov/tree/master/notebooks) with [Python 3.6](https://www.python.org/), [pandas](https://pandas.pydata.org/), [NumPy](http://www.numpy.org/), [Matplotlib](https://matplotlib.org/), and [Graphviz](https://www.graphviz.org/) to generate image files.

For parsing PROV-N files and generating customized `.dot` files with support to the extensions, we use the [Lark parser](https://github.com/erezsh/lark).

Thus, for running the files, please install Python 3.6 and Graphviz, and run:
```
pip install jupyter lark-parser pandas numpy matplotlib
```

To simplify the process of updating readme files, we have markdown files in the ::[source directory](source) with special tags to link and load files.

For updating the project markdowns, please edit the files in the ::[source directory](source) and run:
```
python build.py
```


### Past Development

During the development of ::GET VERSIONED_PROV::, we developed two other extensions with the same goal: ::GET MUTABLE_PROV:: and ::GET INTERTWINED_PROV::.

*[::GET MUTABLE_PROV::](mutable-prov.md)* uses PROV-Dictionary for solving P1 and versioning for solving P2. However, (P3) it adds bidirectional or return edges and (P4) created versions for all entities (including immutable elements).

*[::GET INTERTWINED_PROV::](intertwined-prov.md)*, besides solving P1 and P2, also solves P3 by using interwined versioning (See Figure 7 of https://doi.org/10.1145/280277.280280). However, it still suffers from P4. All in all, it improves the management of complex entities (collections), but has some drawbacks on simple entities (literals and immutable variables).

*::GET VERSIONED_PROV::* does not suffer from any of these problems.

By comparing the number of statements in these approaches:

The ::GET MUTABLE_PROV:: approach has less relationships than ::GET VERSIONED_PROV::. This occurs because ::GET MUTABLE_PROV:: does not have an `entity` for every part of a `value`, and does not use `wasDerivedFrom` relationships in accesses, due to the lach of these `entities`. On the other hand, ::GET MUTABLE_PROV:: has a much bigger number of nodes, due to the addition of `values`.

The ::GET INTERTWINED_PROV:: approach is very similar to the ::GET VERSIONED_PROV::, but the former use explict `Version` entities with `specializationOf` relationships from the entities, while the latter has the version concept implicitly built into the entities, through the checkpoints in `hadMember` relationships. Hence, the ::GET INTERTWINED_PROV:: approach produces much more nodes and relationships than ::GET VERSIONED_PROV::.


Querying with ::GET MUTABLE_PROV:: and ::GET INTERTWINED_PROV:: is as hard as querying with ::GET VERSIONED_PROV::, but they are more powerful than ::GET PLAIN_PROV:: and ::GET PROV_DICTIONARY::.

