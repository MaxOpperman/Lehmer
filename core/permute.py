import argparse

from core.figure_generation_files.rivertz import SetPerm
from core.helper_operations.permutation_graphs import (
    HpathQ,
    count_inversions,
    graph,
    multinomial,
    nonStutterPermutations,
    pathQ,
    perm,
    stutterPermutations,
    total_path_motion,
)
from core.visualization import find_path_colors, plot_graph, visualize


def main():
    """
    Helper tool to find Lehmer paths in neighbor-swap graphs.

    This function takes command line arguments to perform various operations on a given permutation signature.
    It has various options:\n
    - Visualize the NetworkX neighbor swap graph `(--graph)`
    - Compute permutations using Rivertz's algorithm `(--rivertz)`
    - Find paths using Lehmer's algorithm `(--lehmer)`. Here we can also automatically recognize stutters as spurs `(--auto-spur)`
    - Color the nodes in the Lehmer Path `(--color)`, note that `--graph` must be enabled. This automatiaclly enables `--lehmer`.
    - Enable verbose mode `(--verbose)`, here extra information will be printed in the console.
    The input permutation signature is a comma-separated list of integers. (e.g. `4,2,1`)

    Command Line Arguments:

        - ``-s, --signature:`` Input permutation signature (comma separated) *(required)*
        - ``-v, --verbose:`` Enable verbose mode
        - ``-l, --lehmer:`` Compute the path using Lehmer's algorithm
        - ``-a, --auto-spur:`` Automatically recognize stutters as spurs in Lehmer's algorithm
        - ``-g, --graph:`` Show the NetworkX neighbor swap graph
        - ``-c, --color:`` Color the nodes in the Hamiltonian Path based on Lehmer's algorithm
        - ``-r, --rivertz:`` Compute the permutations with Rivertz's algorithm

    Returns:
        None

    Raises:
        ValueError: If the input signature is invalid
    """
    parser = argparse.ArgumentParser(
        description="Helper tool to find paths through permutation neighbor swap graphs."
    )
    parser.add_argument(
        "-s",
        "--signature",
        type=str,
        help="Input permutation signature (comma separated)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose mode (prints all permutations in order)",
    )
    parser.add_argument(
        "-l",
        "--lehmer",
        action="store_true",
        help="Compute the path using Lehmer's algorithm",
    )
    parser.add_argument(
        "-a",
        "--auto-spur",
        action="store_true",
        help="Automatically recognize stutters as spurs",
    )
    parser.add_argument(
        "-g",
        "--graph",
        action="store_true",
        help="Show the NetworkX neighbor swap graph",
    )
    parser.add_argument(
        "-c",
        "--color",
        action="store_true",
        help="Color the nodes in the Hamiltonian Path",
    )
    parser.add_argument(
        "-r",
        "--rivertz",
        action="store_true",
        help="Compute the permutations with Rivertz's algo",
    )

    args = parser.parse_args()
    sig = [int(x) for x in args.signature.split(",")]

    if len(list(sig)) > 0:
        # Compute permutations using Lehmer's algorithm
        if args.lehmer:
            perms = perm(sig)
            stutter = stutterPermutations(sig)
            non_stutter = nonStutterPermutations(sig)
            print(
                f"There are {multinomial(sig)} permutations and computed {len(perms)}, of which {len(stutter)} are "
                f"stutters and {len(non_stutter)} are non-stutters"
            )

        # Compute permutations using Rivertz's algorithm
        if args.rivertz:
            rivertz_perms = []
            for p in SetPerm(sig):
                rivertz_perms.append(p)
            print(
                f"Missed {multinomial(sig) - len(rivertz_perms)} of {multinomial(sig)} permutations; total motion "
                f"{total_path_motion(rivertz_perms)}"
            )
            if pathQ(rivertz_perms):
                print("Rivertz permutations are a path!")
                if HpathQ(rivertz_perms, sig):
                    print("Rivertz permutations are even a Hamiltonian path!")
            else:
                print(
                    "ERROR! Rivertz permutations are not a path (see above for the mistake in the path)"
                )

        # Show the NetworkX neighbor swap graph and color the nodes in the Hamiltonian Path
        if args.graph or args.lehmer:
            perm_graph_dict, edge_color_dict = visualize(
                graph(sig), count_inversions(sig)
            )
            if args.lehmer or args.color:
                node_colors, edge_colors = find_path_colors(
                    edge_color_dict, perm_graph_dict, args, sig
                )
            else:
                node_colors = ["skyblue"] * len(perm_graph_dict.nodes())
                edge_colors = edge_color_dict.values()
            if args.graph:
                plot_graph(perm_graph_dict, node_colors, edge_colors)
    else:
        print("Please provide a valid signature")


if __name__ == "__main__":
    main()
