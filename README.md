# Versioned-PROV

Versioned-PROV is a PROV extension that adds support for the provenance of mutable values by time-versioning entities. This extension is useful to represent fine-grained provenance from scripts with multiple variables refering to the same data structures and nested data-structures.

For more details, please visit the website: [https://dew-uff.github.io/versioned-prov](https://dew-uff.github.io/versioned-prov).

## Authors

- João Felipe Pimentel (Universidade Federal Fluminense)
- Paolo Missier (Newcastle University)
- Leonardo Murta (Universidade Federal Fluminense)
- Vanessa Braganholo (Universidade Federal Fluminense)

## Publications

- [PIMENTEL, J. F. N., MISSIER, P., MURTA, L., & BRAGANHOLO, V.; Versioned-PROV: A PROV extension to support mutable data entities. In International Provenance and Annotation Workshop (IPAW), 2018, London, United Kingdom.](https://github.com/dew-uff/versioned-prov/raw/master/docs/paper.pdf)

## Development

We use [Jupyter Notebooks](https://github.com/dew-uff/versioned-prov/tree/master/notebooks) with [Python 3.6](https://www.python.org/), [pandas](https://pandas.pydata.org/), [NumPy](http://www.numpy.org/), [Matplotlib](https://matplotlib.org/), and [Graphviz](https://www.graphviz.org/) to generate image files.

For parsing PROV-N files and generating customized `.dot` files with support to the extensions, we use [extensible_provn](https://github.com/JoaoFelipe/extensible_provn).

We also use pypandoc to convert markdown files from the [source directory](https://github.com/dew-uff/versioned-prov/raw/master/source) into html.

Thus, for running the files, please install Python 3.6 and Graphviz, and run:
```
pip install jupyter extensible_provn pandas numpy matplotlib pypandoc
```
or in the root of this repository:
```
pip install -e .
```


For updating the project markdowns, please edit the files in the [source directory](https://github.com/dew-uff/versioned-prov/raw/master/source) and run:
```
python build.py
```


### Past Development

During the development of Versioned-PROV, we developed two other extensions with the same goal: Mutable-PROV and Intertwined-PROV.

*[Mutable-PROV](https://dew-uff.github.io/versioned-prov/mutable-prov.html)* uses PROV-Dictionary for solving P1 and versioning for solving P2. However, (P3) it adds bidirectional or return edges and (P4) created versions for all entities (including immutable elements).

*[Intertwined-PROV](https://dew-uff.github.io/versioned-prov/intertwined-prov.html)*, besides solving P1 and P2, also solves P3 by using interwined versioning (See Figure 7 of https://doi.org/10.1145/280277.280280). However, it still suffers from P4. All in all, it improves the management of complex entities (collections), but has some drawbacks on simple entities (literals and immutable variables).

*Versioned-PROV* does not suffer from any of these problems.

By comparing the number of statements in these approaches:

The Mutable-PROV approach has less relationships than Versioned-PROV. This occurs because Mutable-PROV does not have an `entity` for every part of a `value`, and does not use `wasDerivedFrom` relationships in accesses, due to the lach of these `entities`. On the other hand, Mutable-PROV has a much bigger number of nodes, due to the addition of `values`.

The Intertwined-PROV approach is very similar to the Versioned-PROV, but the former use explict `Version` entities with `specializationOf` relationships from the entities, while the latter has the version concept implicitly built into the entities, through the checkpoints in `hadMember` relationships. Hence, the Intertwined-PROV approach produces much more nodes and relationships than Versioned-PROV.


Querying with Mutable-PROV and Intertwined-PROV is as hard as querying with Versioned-PROV, but they are more powerful than Plain PROV and PROV-Dictionary.


## License Terms

License Terms
The MIT License (MIT)

Copyright (c) 2018 Universidade Federal Fluminense (UFF), Newcastle University.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.