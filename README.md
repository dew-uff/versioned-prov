# Versioned-PROV

Versioned-PROV is a PROV extension that adds support for the provenance of mutable values through the timed-versioning of entities. This extension is useful to represent fine-grained provenance from scripts with multiple variables refering to the same data structures and nested data-structures.


PROV does not properly support fine-grained provenance with mutable data structures due the assumption of immutable entities and their representation may become quite verbose. The PROV-Dictionary extension intends to provide data structures support for PROV, but it stills fails to accomodate the mutability of them. In this repository, we propose a new extensions to support the representation of mutable data structures in PROV: Versioned-PROV


*Plain PROV* suffers from two main problems: (P1) when a collection entity is changed, a new collection entity should be created, together with multiple new edges, connecting the new collection entity to the existing or new part entities; and (P2) when more than one variable is assigned to the same collection, and one of the variables changes, all other variables should also change, as they refer to the same memory area, meaning that a new entity should be created for each variable that contains the collection, together with edges for all part entities. Both problems lead to having many extra edges and nodes in the provenance graph.

*PROV-Dictionary* solves the problem P1, but stil sufers from the problem P2.

*Versioned-PROV* solves these problems using a fine-grained versioning strategy.


## Running Example

To describe and evaluate the extension, we use the [Floyd-Warshall](https://github.com/dew-uff/versioned-prov/raw/master/algorithm.py) algorithm. This algorithm calculates the distance of the shortest path between all pairs of nodes in a weighted graph.

By running the Floyd-Warshall in the graph below, and reading the distance between the nodes 0 and 2, it should output 3. By looking at graph, we can see that this path goes from node 0 to node 1 to node 2, instead of using the direct path from node 0 to node 2. However, the Floyd-Warshall algorithm only calculates the distance, and not the paths.

[![Graph](https://github.com/dew-uff/versioned-prov/raw/master/generated/graphs/graph.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/graphs/graph.pdf)

Due the nature of the algorithm, fine-grained provenance can assist in obtained the path. In Floyd-Warshall, considering the nodes `x`, `y`, and `z`, if the sum of the sub-paths `x -> y` and `y -> z` is smaller than the sum of the path `x -> z`, then it updates the value of the path `x -> z` by the sum. Thus, the provenance of the updated `x -> z` should indicate that it was composed by the sum of `x -> y` and `y -> z`.

## Experiment

For our experiment, we collected the provenance of Floyd-Warshall algorithm and mapped it to Plain PROV, PROV-Dictionary, and Versioned-PROV. For descriptions of the mappings, please refer to:
  - [Plain PROV Mapping](prov.md)
  - [PROV-Dictionary Mapping](prov-dictionary.md)
  - [Versioned-PROV Mapping](versioned-prov.md)

We tried to produce the minimum set of PROV-N statements in the mappings without compromising the semantics. For this reason, we use the [Inference 11](https://www.w3.org/TR/prov-constraints/#derivation-generation-use-inference) to avoid using `used` and `wasGeneratedBy` statements when we have `wasDerivedFrom` statements.


The Plain PROV mapping produced the following graph:

[![Floyd-Warshall in Plain PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/floydwarshall.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/floydwarshall.pdf)

The PROV-Dictionary mapping produced the following graph:

[![Floyd-Warshall in PROV-Dictionary](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/floydwarshall.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/floydwarshall.pdf)

The Versioned-PROV mapping produced the following graph:

[![Floyd-Warshall in Versioned-PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/floydwarshall.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/floydwarshall.pdf)

The following table presents the count of each node (entity, activity, value) and relationship (wasDerivedFrom, used, ...) definition in each approach.

Approach|entity|activity|used|was<br>Derived<br>From|was<br>Generated<br>By|had<br>Member|derived<br>By<br>Insertion<br>From
---|---|---|---|---|---|---|---
PROV|123|94|97|125|10|117|0
PROV-Dictionary|124|94|97|105|10|0|39
Versioned-PROV|103|92|103|95|5|18|0


The figure below compares the number of nodes (i.e., `entity`, `activity`, ...) and relationships (i.e., `wasDerivedFrom`, `used`, `wasGeneratedBy`, ...) of each approach. Versioned-PROV is the approach with less componenens. In Versioned-PROV, the `hadMember` relationship with a `checkpoint` indicates the creation of a new version for the entity. Thus, it replaces some entities that exist in the other approaches by this relationship. However, the other approaches also require similar relationships to indicate the membership of elements in data structures. Hence, this replacement does not result in a bigger number of relationships. Additionally, all the other attributes of this approach appear in existing statements of the other approaches. So, the addition of the attributes do not increase the number of components.


[![Comparison of elements](https://github.com/dew-uff/versioned-prov/raw/master/generated/graphs/paper_comparison.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/graphs/paper_comparison.pdf)


The PROV-Dictionary approach creates a new `entity` when there is a change on an existing `entity` and when there is an access to an `entity` that represents a data-structure. Thus, it presents more nodes and relationships than Versioned-PROV. However, it presents less relationships than the Plain PROV approach. This occurs because, the Plain PROV also creates new `entities` on changes, but has no mechanisms to indicate that an `entity` has all members of the previously existing `entity`, thus it requires many `hadMember` relationship for every `entity` that represent data structures. The number of nodes in Plain PROV and PROV-Dictionary could be equivalent, however, according to the PROV-Dictionary specification, for a dictionary to be deterministic, its derivation chain should end in an `EmptyDictionary` `entity`. Hence, we need one extra node for the PROV-Dictionary approach.


For an in depth analaysis of space requirements of these approaches, please take a a look at our [Comparison](comparison.md).


## Query

As stated before, the access `result[0][2]` represents de distance of the shortest path between the node 0 and the node 2 in the graph. This access is represented by the entity `result_a020` in our mappings.
The provenance query of this entity should indicate which other parts of the graph were used to construct the shortest path, thus indicating the path. The following figures present the query result in each mapping.

The Plain PROV mapping produces the following query result:

[![Query in Plain PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/plain_prov/query.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/plain_prov/query.pdf)

The PROV-Dictionary mapping produces the following query result:

[![Query in PROV-Dictionary](https://github.com/dew-uff/versioned-prov/raw/master/generated/prov_dictionary/query.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/prov_dictionary/query.pdf)


The Versioned-PROV mapping produces the following query result:

[![Query in Versioned-PROV](https://github.com/dew-uff/versioned-prov/raw/master/generated/versioned_prov/query.png)](https://github.com/dew-uff/versioned-prov/blob/master/generated/versioned_prov/query.pdf)

Querying with Versioned-PROV is harder than querying with Plain PROV, and PROV-Dictionary, since the former mapping may include cycles and requires navigating through different edges. However, these mappings allow better derivation queries, by identifing that an entity that was generated as a part of a data structure was derived from the data structure, without deriving from the other parts of the data structure. Due the lack of support for this kind of derivation in Plain PROV and PROV-Dictionary, we opted to omit membership derivations in the first two figures of this section.

## Unfold

As stated before, the Versioned-PROV mapping produces less nodes for the Floyd-Warshall algorithm and supports more meaningful queries. However, it is complete enough to be unfolded into the Plain PROV mapping. If membership querying is not required, unfolding the Versioned-PROV mapping may be a good option to improve the performance of queries, since Plain PROV is a DAG.


## Development

We use [Jupyter Notebooks](https://github.com/dew-uff/versioned-prov/tree/master/notebooks) with [Python 3.6](https://www.python.org/), [pandas](https://pandas.pydata.org/), [NumPy](http://www.numpy.org/), [Matplotlib](https://matplotlib.org/), and [Graphviz](https://www.graphviz.org/) to generate image files.

For parsing PROV-N files and generating customized `.dot` files with support to the extensions, we use the [Lark parser](https://github.com/erezsh/lark).

Thus, for running the files, please install Python 3.6 and Graphviz, and run:
```
pip install jupyter lark-parser pandas numpy matplotlib
```

To simplify the process of updating readme files, we have markdown files in the [source directory](https://github.com/dew-uff/versioned-prov/raw/master/source) with special tags to link and load files.

For updating the project markdowns, please edit the files in the [source directory](https://github.com/dew-uff/versioned-prov/raw/master/source) and run:
```
python build.py
```


### Past Development

During the development of Versioned-PROV, we developed two other extensions with the same goal: Mutable-PROV and Intertwined-PROV.

*[Mutable-PROV](mutable-prov.md)* uses PROV-Dictionary for solving P1 and versioning for solving P2. However, (P3) it adds bidirectional or return edges and (P4) created versions for all entities (including immutable elements).

*[Intertwined-PROV](intertwined-prov.md)*, besides solving P1 and P2, also solves P3 by using interwined versioning (See Figure 7 of https://doi.org/10.1145/280277.280280). However, it still suffers from P4. All in all, it improves the management of complex entities (collections), but has some drawbacks on simple entities (literals and immutable variables).

*Versioned-PROV* does not suffer from any of these problems.

By comparing the number of statements in these approaches:

The Mutable-PROV approach has less relationships than Versioned-PROV. This occurs because Mutable-PROV does not have an `entity` for every part of a `value`, and does not use `wasDerivedFrom` relationships in accesses, due to the lach of these `entities`. On the other hand, Mutable-PROV has a much bigger number of nodes, due to the addition of `values`.

The Intertwined-PROV approach is very similar to the Versioned-PROV, but the former use explict `Version` entities with `specializationOf` relationships from the entities, while the latter has the version concept implicitly built into the entities, through the checkpoints in `hadMember` relationships. Hence, the Intertwined-PROV approach produces much more nodes and relationships than Versioned-PROV.


Querying with Mutable-PROV and Intertwined-PROV is as hard as querying with Versioned-PROV, but they are more powerful than Plain PROV and PROV-Dictionary.