import argparse

from cycle_cover import get_connected_cycle_cover
from helper_operations.path_operations import cycleQ, pathQ
from helper_operations.permutation_graphs import (
    get_perm_signature,
    multinomial,
    stutterPermutations,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connects the cycle cover to a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph."
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
        "-n",
        "--naive-glue",
        action="store_true",
        help="Naively glue the disjoint cycle cover (when the attempted edge is not connected in the subcycle).",
    )
    args = parser.parse_args()
    sig = tuple([int(x) for x in args.signature.split(",")])
    connected_cycle_cover = get_connected_cycle_cover(sig, args.naive_glue)
    if args.verbose:
        print(f"Connected cycle cover: {connected_cycle_cover}")
    stut_count = len(stutterPermutations(sig))
    print(
        f"Cycle cover is a cycle {cycleQ(connected_cycle_cover)} and a path {pathQ(connected_cycle_cover)} "
        f"with {len(connected_cycle_cover)}/{multinomial(sig)} (incl {stut_count} stutters is {stut_count+len(connected_cycle_cover)}) permutations from signature {get_perm_signature(connected_cycle_cover[-1])}."
    )
