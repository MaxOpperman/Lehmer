import itertools

from core.helper_operations.path_operations import get_transformer, transform
from core.stachowiak import _lemma10_helper, lemma2_extended_path
from core.steinhaus_johnson_trotter import SteinhausJohnsonTrotter
from core.type_variations.verhoeff_list import HpathNS


def lemma10(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Computes Lemma 10 by Stachowiak:
    If `q = |Q| > 2`, `Q` is even and `GE(Q)` contains a Hamiltonian path and `p > 0` then `GE(Q|l^p)` has a Hamiltonian cycle.
    Here `Q` is two elements in the signature that form a Hamiltonian path of even length and p is the third element.

    Args:
        sig (tuple[int, ...]):
            The signature of the graph; `Q` is the first two elements, `p` is the third.
            `Q` is of length 2, its colors are 0 and 1. It contains a Hamiltonian path.
            `p` is the third element of sig and has color 2 and occurs `p` times.

    Returns:
        list[tuple[int, ...]]:
            A Hamiltonian cycle in the neighbor-swap graph of the form `GE(Q|l^p)`

    Raises:
        AssertionError:
            If the signature is not well-formed. The first two elements must be able to form a Hamiltonian path of even length > 2.
    """
    K = [tuple(row) for row in HpathNS(sig[0], sig[1])]
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Finds a Hamiltonian cycle in a graph using Lemma 11 from Stachowiak's paper:
    If `q = |Q| > 2`, `p = |P| > 0` and `GE(Q)` has an even number of vertices and contains a Hamiltonian path then `GE(Q|P)` has a Hamiltonian cycle.

    Args:
        sig (tuple[int, ...]):
            A signature of a neighbor-swap graph where at least two elements form a Hamiltonian path of even length > 2.
            These two elements are set to the front of the signature using a recursive call.
            Note that this can also be three elements if the first two are 1 (using Lemma 2). Or at least 3 elements that occur once (using Steinhaus-Johnson-Trotter algorithm).
            The rest of the signature is processed using Stachowiak's lemmas.

    Returns:
        list[tuple[int, ...]]:
            A Hamiltonian cycle in the neighbor-swap graph of the form `GE(Q|P)`. `Q` is this Hamiltonian path and `P` is the rest of the signature

    Raises:
        ValueError: If the signature is empty.
        ValueError: There are no elements that can form a Hamiltonian path.

    Notes:
        - If `q = |Q| > 2`, `p = |P| > 0` and `GE(Q)` has an even number of vertices and contains a Hamiltonian path, then `GE(Q|P)` has a Hamiltonian cycle.
        - The function first checks the length of the signature and handles special cases where the signature has only one or two elements.
        - If the signature is not ordered well, it transforms the signature and recursively calls the function with the transformed signature. The order is well when the first two elements are the largest odd numbers.
        - If the first two elements in the signature can form a cycle (more than two permutations), it uses Verhoeff's Theorem to find the cycle.
        - If the first 3 (or more) elements are 1, it uses the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle.
        - If the third element in the signature is not 0, it uses Stachowiak's Lemma 2 to find a Hamiltonian path in `GE(Q|l^{sig[2]})`.
        - Finally, it iterates over the remaining elements in the signature and calls the helper function _lemma10_helper to extend the cycle.

    References:
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017. (Used to find Hamiltonian cycles in binary neighbor-swap graphs.)
    """
    if len(list(sig)) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(list(sig)) == 1:
        return []
    elif len(list(sig)) == 2 and sig[0] == sig[1] == 1:
        return [(0, 1), (1, 0)]
    elif sum(1 for n in sig if n % 2 == 1) < 2:
        raise ValueError("At least two odd numbers are required for Lemma 11")
    # index the numbers in the signature such that we can transform them back later
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])

    # if the order is optimal (i.e. the first two elements are the largest odd numbers)
    # and the number of odd numbers is at least 2
    if sig != sorted_sig:
        # return that solution given by this lemma (transformed, if needed)
        return transform(lemma11(sorted_sig), transformer)
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
