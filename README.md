# Permutation generation by neighbor-swaps
Gruaduation project about finding Lehmer's paths on neighbor-swap graphs of permutation generation.

## Permute.py
The `permute.py` script mainly functions as a visualization tool for neighbor-swap graphs of permutations.
Graphs can be visualized and paths constructed by Lehmer's algorithm (which unfortunately doesn't work for cases with more than 7 elements) can be shown.
One can also construct a path by clicking nodes or edges (or right-clicking nodes). By pressing the `C` key all nodes are reset to their original color.

### Usage
Run the `permute.py` script with the following command-line arguments (only the first is required):

- `-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode.
- `-l, --lehmer`: Compute the path using Lehmer's algorithm.
- `-a, --auto-spur`: Automatically recognize stutters as spurs (if the `--lehmer` parameter is passed).
- `-g, --graph`: Show the NetworkX neighbor swap graph.
- `-c, --color`: Color the nodes in the Hamiltonian Path.
- `-r, --rivertz`: Compute the permutations with Rivertz's algorithm.

## Stachowiak.py
Run the `stachowiak.py` script with the following command-line arguments:

- `-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode.

Stachowiak.py uses the code from `verhoeff.py` to compute the neighbor-swap paths for the binary case (two colors).
Then the lemmas from Stachowiak (Hamilton paths in graphs of linear extensions for unions of posets, 1992) are used to add elements to this path.
To be exact, lemma 7, 8, 9, 10, and 11 are used to achieve this. But Lemma 2 is also programmed as a function of the script.

### Testing
For testing, the Pytest library was used. By running `pytest`, all tests are executed. Some tests are marked as slow.
The slow tests can be executed seperately with `pytest -m slow` or excluded with `pytest -m "not slow"`.
Currently, tests are written only for Lemma 11, which uses the lemmas 7, 8, 9, and 10.
The code also uses helper functions made by Ana Smerdu (Hamiltonian cycles in neighbor-swap graphs, 2019).
These functions are tested too by their provided tests.

