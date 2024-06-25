import argparse
import itertools
import math

from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    cycleQ,
    pathQ,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import multinomial
from stachowiak import _lemma10_helper, lemma2_extended_path
from steinhaus_johnson_trotter import SteinhausJohnsonTrotter
from type_variations.verhoeff_list import HpathNS


def lemma10(sig: list[int]) -> list[tuple[int, ...]]:
    """If q = |Q| > 2, Q is even and GE(Q) contains a Hamiltonian path and p > 0 then GE(Q|l^p) has a Hamiltonian cycle."""
    K = [tuple(row) for row in HpathNS(sig[0], sig[1])]
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: list[int]) -> list[tuple[int, ...]]:
    """If q = |Q| > 2, p = |P| > 0 and GE(Q) has an even number of vertices and contains a Hamiltonian path then GE(Q|P) has a Hamiltonian cycle."""
    if len(sig) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(sig) == 1:
        return [(0,) * sig[0]]
    elif len(sig) == 2 and sig[0] == sig[1] == 1:
        return [(0, 1), (1, 0)]
    elif sum(1 for n in sig if n % 2 == 1) < 2:
        raise ValueError("At least two odd numbers are required for Lemma 11")
    # index the numbers in the signature such that we can transform them back later
    indexed_sig = [(value, idx) for idx, value in enumerate(sig)]
    # put the odd numbers first in the signature
    indexed_sig.sort(reverse=True, key=lambda x: [x[0] % 2, x[0]])

    # if the order is optimal (i.e. the first two elements are the largest odd numbers)
    # and the number of odd numbers is at least 2
    if sig != [x[0] for x in indexed_sig]:
        # if the order contains trailing 0's, remove them
        while indexed_sig[-1][0] == 0:
            indexed_sig.pop()
        # return that solution given by this lemma (transformed, if needed)
        return transform(
            lemma11([x[0] for x in indexed_sig]), [x[1] for x in indexed_sig]
        )
    # if the first two elements in the signature can form a cycle (so more than two permutations)
    if sum(sig[:2]) > 2:
        path = [tuple(row) for row in HpathNS(sig[0], sig[1])]  # K in the paper
        next_color = 2
    elif sum(1 for n in sig if n % 2 == 1) > 2:
        # use the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle if the first 3 (or more) elements are 1
        try:
            next_color = sig.index(next(x for x in sig if x != 1))
        except StopIteration:
            next_color = len(sig)  # all elements are 1
        path = SteinhausJohnsonTrotter.get_sjt_permutations(
            SteinhausJohnsonTrotter(), next_color
        )
    elif sig[2] != 0:
        # use Stachowiak's lemma 2 to find a Hamiltonian path in GE(Q|P[1])
        path = lemma2_extended_path(tuple([2] * sig[2]))
        next_color = 3
    else:
        raise ValueError(
            "q = |Q| > 2 and GE(Q) has an even number of vertices is required for Lemma 11"
        )
    for ind, new_color in enumerate(sig[next_color:], start=next_color):
        cycle = _lemma10_helper(path, new_color, ind)
        path = cycle
    return path


if __name__ == "__main__":
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

    args = parser.parse_args()
    s = [int(x) for x in args.signature.split(",")]
    if len(s) > 1:
        if len(s) == 2:
            perms_odd = HpathNS(s[0], s[1])
            if args.verbose:
                print(f"Resulting path {perms_odd}")
            print(
                f"Verhoeff's result for k0={s[0]} and k1={s[1]}: {len(set(tuple(row) for row in perms_odd))}/{len(perms_odd)}/{math.comb(s[0] + s[1], s[1])} "
                f"is a path: {pathQ(perms_odd)} and a cycle: {cycleQ(perms_odd)}"
            )
        elif s[0] % 2 == 0 or s[1] % 2 == 0:
            raise ValueError(
                "The first two elements of the signature should be odd for Stachowiak's permutations"
            )
        else:
            l11 = lemma11(s)
            if args.verbose:
                print(f"lemma 11 results {l11}")
            print(
                f"lemma 11 {len(set(l11))}/{len(l11)}/{multinomial(s)} is a path: {pathQ(l11)} and a cycle: {cycleQ(l11)}"
            )
