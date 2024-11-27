# Permutation generation by neighbor-swaps
[![PyTest](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MaxOpperman/9010143336585a9f9ff81a9ec805a0b0/raw/lehmer-test-status.json)](https://github.com/MaxOpperman/Lehmer/actions/workflows/python-tests.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MaxOpperman/9010143336585a9f9ff81a9ec805a0b0/raw/lehmer-coverage.json)](https://github.com/MaxOpperman/Lehmer/actions/workflows/python-tests.yml)
[![Docs Updated](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MaxOpperman/9010143336585a9f9ff81a9ec805a0b0/raw/lehmer-docs-status.json)](https://maxopperman.github.io/Lehmer/)

This is my Gruaduation Project about finding Lehmer's paths in neighbor-swap graphs. This proof's Lehmer's conjecture that a graph where permutations represent nodes and edges are drawn for possible neighbor-swaps admits an 'imperfect' Hamiltonian path. The nodes that cannot be visited in a Hamiltonian path can be incorporated as single spurs (at distance one from the path). This project is primarily based on articles by T. Verhoeff: [The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations](https://doi.org/10.1007/s10623-016-0301-9) and by G. Stachowiak [Hamilton Paths in Graphs of Linear Extensions for Unions of Posets](https://doi.org/10.1137/0405016). We also prove Verhoeff's conjecture:

*For every neighbor-swap graph, the subgraph consisting of its non-stutter permutations admits a Hamiltonian path. Furthermore, there even exists a Hamiltonian cycle on the non-stutter permutations, except when:*

1. *The signature arity is zero or one, or*
2. *The signature is binary, and at least one of the \( k_i \) is odd, or*
3. *The signature is a permutation of \( (2k, 1, 1) \).*

And thus we also prove Lehmer's conjecture:
*A path/cycle, possibly with single spurs, that visits the spur bases twice and all other vertices once can be constructed for every neighbor-swap graph.*

## Lehmer Paths
Run `python lehmer_paths.py` with the following arguments:

- *`-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode (prints all permutations in order).

This will return a Lehmer path in a neighbor-swap graph is a path/cycle, possibly with single spurs, that visits the spur bases twice and all other vertices once. The stutter permutations are the spur tips. This is new work from my Graduation Project.


## Hamiltonian cycle on the non-stutter permutations
Run `python connect_cycle_cover.py` with the following arguments:

- *`-s, --signature`: Input permutation signature (comma-separated).
- `-n, --naive-glue`: Naively glue the disjoint cycle cover (when the attempted edge is not connected in the subcycle).
- `-v, --verbose`: Enable verbose mode (prints all permutations in order).

This will return a Hamiltonian cycle on the non-stutter permutations. The signatures *(2, 2, 1, 1, 1)* and *(3, 3, 3, 2)* throw errors because they use incorrect cross edges. This is new work from my Graduation Project.


## Disjoint Cycle Cover
Run `python cycle_cover.py` with the following arguments:

- *`-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode (prints all permutations in order).

This will return a list of cycles of depth 1. We know that the subcycle level contains a Hamiltonian cycle on the non-stutter permutations by Verhoeff's proof in his earlier mentioned [work](https://doi.org/10.1007/s10623-016-0301-9). This implementation is new.


## Stachowiak's Theorem
Run `python stachowiak.py` with the following command-line arguments:

- *`-s, --signature`: Input permutation signature (comma-separated), the sum of first two colors be even and > 2 (to allow for a Hamiltonian path).
- `-v, --verbose`: Enable verbose mode (print all permutations).

Our implementation of Stachowiak's algorithm uses the code from `verhoeff.py` to compute the Hamiltonian paths in neighbor-swap graphs of binary signatures (i.e. with two colors). It might also use `steinhaus_johnson_trotter.py` if the first 3 (or more consecutive) numbers are equal to 1.
When using this to compute Hamiltonian paths, note that it is required that the number of multiset permutations is required to be **even and > 2** (see Lemma 10 by Stachowiak on why this is required).
Then the lemmas from Stachowiak ([Hamilton paths in graphs of linear extensions for unions of posets, 1992](https://doi.org/10.1137/0405016)) are used to add elements to this path.
To be exact, lemma 7, 8, 9, 10, and 11 are used to achieve this. But Lemma 2 is also programmed as a function of the script. This implementation is new.


## Verhoeff Cycle Cover Edge Cases
`python ./figure_generation_files/verhoeffCycleCover.py` visualizes the Figures 11 and 12 from [Verhoeff's work](https://doi.org/10.1007/s10623-016-0301-9). These paths are later also used in the Graduation Project.

Usage:

- *`-e, --even`: Input integer. Must be even by definition of the paths.
- `-c, --combine`: Combine Figure 11 and 12 into one graph. (`False` by default and sequentially displays the images)
- `-s, --save`: Save the generated images and don't display them if `True`. (`False` by default)
- `-m, --merge`: Merge the graphs into one plot.
- `-c, --cycle`: Generate a cycle instead of a path for the *(odd, 2, 1)* signatures.


## Permute.py
The `permute.py` script mainly functions as a visualization tool for simple neighbor-swap graphs of permutations.
Graphs can be visualized and paths constructed by Lehmer's algorithm (which unfortunately doesn't work for cases with more than 7 elements) can be shown.
One can also construct a path by clicking nodes or edges (or right-clicking nodes). By pressing the `C` key all nodes are reset to their original color.

### Usage
Run the `permute.py` script with the following command-line arguments (only the first is required, indicated using the *):

- *`-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode.
- `-l, --lehmer`: Compute the path using Lehmer's algorithm. (Shows that the algorithm does not work for n > 7)
- `-a, --auto-spur`: Automatically recognize stutters as spurs (if the `--lehmer` parameter is passed).
- `-g, --graph`: Show the NetworkX neighbor swap graph.
- `-c, --color`: Color the nodes in the Hamiltonian Path.
- `-r, --rivertz`: Compute the permutations with Rivertz's algorithm.


## Testing
For testing, the Pytest library was used. By running `pytest`, all tests are executed. Some tests are marked as slow.
The slow tests can be executed seperately with `pytest -m slow` or excluded with `pytest -m "not slow"`.
To generate a coverage report: `pytest --cov-report=html --cov=./ tests/` with optional pytest parameters, e.g. `-m "not slow"`.

The code also uses helper functions made by Ana Smerdu [Hamiltonian cycles in neighbor-swap graphs, 2019](https://repozitorij.uni-lj.si/IzpisGradiva.php?id=108786). These functions are tested too by their provided tests.


### Type variations
There are multiple variations on Stachowiak's algorithm using different Python types. Using `python ./figure_generation_files/timetests.py` these variations can be compared. The following arguments can be passed:

- `-l, --latex`: Generate LaTeX tables for the results (`False` by default)
- `-g, --graph`: Generate graphs for the results and save them (`False` by default)
- `-n, --numpy`: Incluce numpy in the tests (`False` by default)

All results are stored in `./out`. Then Numpy files are too slow to give a good comparison of the rest, so the option is given to leave out these tests.


## Generate the Documentation
The docs are published online at via GitHub: [Read the docs](https://maxopperman.github.io/Lehmer).

Run `pip install -r requirements.txt && cd docs && sphinx-apidoc -o . .. ../*tests* && ./make.bat html`. Or consecutively:
```
pip install -r requirements.txt
cd docs
sphinx-apidoc -o . .. ../*tests*
./make.bat html
```
For Linux use the `Makefile` instead.
To actually build the documentation use: `sphinx-apidoc -o . .. ../*tests* && sphinx-build -b html docs/ docs/_build` instead of either running the makefile.