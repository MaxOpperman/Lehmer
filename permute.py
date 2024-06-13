import argparse

from helper_operations.permutation_graphs import (
    HpathQ,
    count_inversions,
    graph,
    multinomial,
    non_stutters,
    pathQ,
    perm,
    stutters_sig,
    total_path_motion,
)
from rivertz import SetPerm
from visualization import find_path_colors, plot_graph, visualize

if __name__ == "__main__":
    lehmer_strategy_help = "Default: random choices\r\n"
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
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
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
    if len(sig) > 0:
        perms = perm(sig)
        stutter = stutters_sig(sig)
        non_stutter = non_stutters(sig)
        print(
            f"There are {multinomial(sig)} permutations and computed {len(perms)}, of which {len(stutter)} are "
            f"stutters and {len(non_stutter)} are non-stutters"
        )

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
                    print("Rivertz permutations are even a Hamiltonian path!!!")
            else:
                print(
                    "ERROR! Rivertz permutations are not a path (see above for the mistake in the path)"
                )
        if args.graph or args.lehmer:
            perm_graph_dict, edge_color_dict = visualize(
                graph(sig), count_inversions(sig)
            )
            if args.lehmer:
                node_colors, edge_colors = find_path_colors(
                    edge_color_dict, perm_graph_dict, args, sig
                )
            else:
                node_colors = ["k" for node in perm_graph_dict.nodes()]
                edge_colors = edge_color_dict.values()
            if args.graph:
                plot_graph(perm_graph_dict, node_colors, edge_colors)
    else:
        print("Please provide a valid signature")
