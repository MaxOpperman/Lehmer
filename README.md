# Permutation generation by neighbor-swaps
![PyTest](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MaxOpperman/9010143336585a9f9ff81a9ec805a0b0/raw/lehmer-test-status.json)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MaxOpperman/9010143336585a9f9ff81a9ec805a0b0/raw/lehmer-coverage.json)

Gruaduation project about finding Lehmer's paths on neighbor-swap graphs of permutation generation.
Primarily based on articles by T. Verhoeff: [The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations](https://doi.org/10.1007/s10623-016-0301-9) and by G. Stachowiak [Hamilton Paths in Graphs of Linear Extensions for Unions of Posets](https://doi.org/10.1137/0405016).

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

## Permute.py
The `permute.py` script mainly functions as a visualization tool for neighbor-swap graphs of permutations.
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

## Stachowiak.py
Run the `stachowiak.py` script with the following command-line arguments:

- *`-s, --signature`: Input permutation signature (comma-separated), the sum of first two colors be even and > 2 (to allow for a Hamiltonian path).
- `-v, --verbose`: Enable verbose mode.

Stachowiak.py uses the code from `verhoeff.py` to compute the neighbor-swap paths for the binary case (two colors). It might also use `steinhaus_johnson_trotter.py` if the first 3 (or more consecutive) numbers are equal to 1.
When using this to compute Hamiltonian paths, note that it is required that the number of linear extensions of `Q` is required to be even and > 2 (see Lemma 10 by Stachowiak on why this is required).
Then the lemmas from Stachowiak (Hamilton paths in graphs of linear extensions for unions of posets, 1992) are used to add elements to this path.
To be exact, lemma 7, 8, 9, 10, and 11 are used to achieve this. But Lemma 2 is also programmed as a function of the script.

### Type variations
There are multiple variations on Stachowiak's algorithm using different Python types. Using `python ./figure_generation_files/timetests.py` these variations can be compared. The following arguments can be passed:

- `-l, --latex`: Generate LaTeX tables for the results (`False` by default)
- `-g, --graph`: Generate graphs for the results and save them (`False` by default)
- `-n, --numpy`: Incluce numpy in the tests (`False` by default)

All results are stored in `./out`. Then Numpy files are too slow to give a good comparison of the rest, so the option is given to leave out these tests.

### Testing
For testing, the Pytest library was used. By running `pytest`, all tests are executed. Some tests are marked as slow.
The slow tests can be executed seperately with `pytest -m slow` or excluded with `pytest -m "not slow"`.
Currently, tests are written only for selected type variations. These are lists of tuples (for both Verhoeff and Stachowiak), and numpy arrays.
To generate a coverage report: `pytest --cov-report=html --cov=./ tests/` with optional pytest parameters, e.g. `-m "not slow"`.

The code also uses helper functions made by Ana Smerdu (Hamiltonian cycles in neighbor-swap graphs, 2019).
These functions are tested too by their provided tests.

## cycle_cover.py
Run `python cycle_cover.py` with the following arguments:

- *`-s, --signature`: Input permutation signature (comma-separated).
- `-v, --verbose`: Enable verbose mode.

This will return a list of cycles of unknown depth. We know that the lowest level contains only cycles by Verhoeff's proof in his earlier mentioned [work](https://doi.org/10.1007/s10623-016-0301-9).


## Verhoeff Cycle Cover Edge Cases
`python ./figure_generation_files/verhoeffCycleCover.py` visualizes the Figures 11 and 12 from [Verhoeff's work](https://doi.org/10.1007/s10623-016-0301-9). These paths are later also used in `cycle_cover.py`.

Usage:

- *`-e, --even`: Input integer. Must be even by definition of the paths.
- `-c, --combine`: Combine Figure 11 and 12 into one graph. (`False` by default and sequentially displays the images)
- `-s, --save`: Save the generated images and don't display them if `True`. (`False` by default)
