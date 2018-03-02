# Mutable-PROV

Mutable-PROV is a PROV extension that adds support for mutable values provenance. This extension is useful to represent fine-grained provenance from scripts with multiple variables refering to the same data structures and nested data-structures.


PROV does not properly support fine-grained provenance with mutable data structures due the assumption of immutable entities and their representation may become quite verbose. The PROV-Dictionary extension intends to provide data structures support for PROV, but it stills fails to accomodate the mutability of them. Thus, we propose Mutable-PROV to support the representation of mutable data structures in PROV.

## Running Example

To describe and evaluate the extension, we use the [Floyd-Warshall](https://github.com/dew-uff/mutable-PROV/tree/master/algorithm.py) algorithm. This algorithm calculates the distance of the shortest path between all pairs of nodes in a weighted graph.

By running the Floyd-Warshall in the graph below, and reading the distance between the nodes 0 and 2, it should output 3. By looking at graph, we can see that this path goes from node 0 to node 1 to node 2, instead of using the direct path from node 0 to node 2. However, the Floyd-Warshall algorithm only calculates the distance, and not the paths.

[![Graph](https://github.com/dew-uff/mutable-prov/raw/master/graphs/graph.png)](https://github.com/dew-uff/mutable-prov/raw/master/graphs/graph.svg)

Due the nature of the algorithm, fine-grained provenance can assist in obtained the path. In Floyd-Warshall, considering the nodes `x`, `y`, and `z`, if the sum of the sub-paths `x -> y` and `y -> z` is smaller than the sum of the path `x -> z`, then it updates the value of the path `x -> z` by the sum. Thus, the provenance of the updated `x -> z` should indicate that it was composed by the sum of `x -> y` and `y -> z`.

## Experiment

For our experiment, we collected the provenance of Floyd-Warshall algorithm and mapped it to plain PROV, PROV-Dicitionary, Mutable-PROV, Explicit-Versioned-PROV, Versioned-PROV. For descriptions of the mappings, please refer to [Plain PROV Mapping](prov.md), [PROV-Dictionary Mapping](prov-dictionary.md), [Mutable-PROV Mapping](mutable-prov.md), [Explicit-Versioned-PROV Mapping](explicit-versioned-prov.md), and [Versioned-PROV Mapping](versioned-prov.md).


The plain PROV mapping produced the following graph:

[![Floyd-Warshall in Plain PROV](https://github.com/dew-uff/mutable-prov/raw/master/plain_prov/floydwarshall.png)](https://github.com/dew-uff/mutable-prov/raw/master/plain_prov/floydwarshall.svg)
(Click on the image for a svg version)

The PROV-Dictionary mapping produced the following graph:

[![Floyd-Warshall in PROV-Dictionary](https://github.com/dew-uff/mutable-prov/raw/master/prov_dictionary/floydwarshall.png)](https://github.com/dew-uff/mutable-prov/raw/master/prov_dictionary/floydwarshall.svg)
(Click on the image for a svg version)

The Mutable-PROV mapping produced the following graph:

[![Floyd-Warshall in Mutable-PROV](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/floydwarshall.png)](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/floydwarshall.svg)
(Click on the image for a svg version)

The following table presents the count of each node (entity, activity, value) and relationship (wasDerivedFrom, used, ...) definition in each approach.

Approach|entity|activity|value|used|was<br>Derived<br>From|was<br>Generated<br>By|had<br>Member|derived<br>By<br>Insertion<br>From|accessed<br>Part|accessed|defined|was<br>Defined<br>By|derived<br>By<br>Insertion
---|---|---|---|---|---|---|---|---|---|---|---|---|---
PROV|242|212|0|488|244|232|126|0|0|0|0|0|0
PROV-Dictionary|276|212|0|491|244|235|0|45|0|0|0|0|0
Mutable-PROV|216|211|41|336|101|210|0|0|134|47|35|35|8


The figure below compares the elements of each approach. Note that Mutable-PROV reduces the number of PROV nodes and relationships in comparision to the other approaches, but it does impose an overhead with values and values relationships for all entities. Overall, the amount of elements in Mutable-PROV is comparable to the amount of elements in PROV-Dictionary in our example. Mutable-PROV has an advantage in algorithms with more data structure updates while PROV-Dictionary han an advantage in algorithms with more simple variables.


[![Comparison of elements](https://github.com/dew-uff/mutable-prov/raw/master/graphs/comparison.png)](https://github.com/dew-uff/mutable-prov/raw/master/graphs/comparison.svg)


## Query

As stated before, the access `result[0][2]` represents de distance of the shortest path between the node 0 and the node 2 in the graph. This access is represented by the entity `result_a020` in our mappings.
The provenance query of this entity should indicate which other parts of the graph were used to construct the shortest path, thus indicating the path. The following figures present the query result in each mapping.

The plain PROV mapping produces the following query result:

[![Query in Plain PROV](https://github.com/dew-uff/mutable-prov/raw/master/plain_prov/query.png)](https://github.com/dew-uff/mutable-prov/raw/master/plain_prov/query.svg)

The PROV-Dictionary mapping produces the following query result:

[![Query in PROV-Dictionary](https://github.com/dew-uff/mutable-prov/raw/master/prov_dictionary/query.png)](https://github.com/dew-uff/mutable-prov/raw/master/prov_dictionary/query.svg)

The Mutable-PROV mapping produces the following query result:

[![Query in Mutable-PROV](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/query.png)](https://github.com/dew-uff/mutable-prov/raw/master/mutable_prov/query.svg)


The Mutable-PROV query is the hardest, as it requires controlling cycles and navigating through different edges. However, it produces less nodes than the others, which may be good to not overwhelm users. For queries, the PROV-Dictionary mapping is a better option, since queries can keep the assumption of a simple DAG, and the amount of resulting nodes is close to that produced in Mutable-PROV.


## Development

We use [Jupyter Notebooks](https://github.com/dew-uff/mutable-PROV/tree/master/notebooks) with [Python 3.6](https://www.python.org/), [pandas](https://pandas.pydata.org/), [NumPy](http://www.numpy.org/), [Matplotlib](https://matplotlib.org/), and [Graphviz](https://www.graphviz.org/) to generate image files.

For parsing PROV-N files and generating customized `.dot` files with support to the extensions, we use the [Lark parser](https://github.com/erezsh/lark).

Thus, for running the files, please install Python 3.6 and Graphviz, and run:
```
pip install jupyter lark-parser pandas numpy matplotlib
```
