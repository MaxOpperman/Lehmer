from helper_operations.path_operations import get_transformer
from type_variations.stachowiak_list import (
    _lemma10_helper,
    lemma2_extended_path,
    transform_list,
)
from type_variations.steinhaus_johnson_trotter_list import SteinhausJohnsonTrotterList
from verhoeff import HpathNS


def lemma10(sig: list[int]):
    """If q = |Q| > 2, Q is even and GE(Q) contains a Hamiltonian path and p > 0 then GE(Q|l^p) has a Hamiltonian cycle."""
    K = [list(tuple_perm) for tuple_perm in HpathNS(sig[0], sig[1])]
    cycle = _lemma10_helper(K, sig[2], 2)
    return cycle


def lemma11(sig: list[int]) -> list[list[int]]:
    """If q = |Q| > 2, p = |P| > 0 and GE(Q) has an even number of vertices and contains a Hamiltonian path then GE(Q|P) has a Hamiltonian cycle."""
    if len(sig) == 0:
        raise ValueError("Signature must have at least one element")
    elif len(sig) == 1:
        return [[0] * sig[0]]
    elif len(sig) == 2 and sig[0] == sig[1] == 1:
        return [[0, 1], [1, 0]]
    elif sum(1 for n in sig if n % 2 == 1) < 2:
        raise ValueError("At least two odd numbers are required for Lemma 11")
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])

    # if the order is optimal (i.e. the first two elements are the largest odd numbers)
    # and the number of odd numbers is at least 2

    if sig != sorted_sig:
        # return that solution given by this lemma (transformed, if needed)
        return transform_list(lemma11(sorted_sig), transformer)
    elif sum(sig[:2]) > 2:
        path = [
            list(tuple_perm) for tuple_perm in HpathNS(sig[0], sig[1])
        ]  # K in the paper
        next_color = 2
    elif sig[2] == 1:
        # use the Steinhaus-Johnson-Trotter algorithm to get the Hamiltonian cycle if the first 3 (or more) elements are 1
        try:
            next_color = sig.index(next(x for x in sig if x != 1))
        except StopIteration:
            next_color = len(sig)  # all elements are 1
        path = SteinhausJohnsonTrotterList.get_sjt_permutations(
            SteinhausJohnsonTrotterList(), next_color
        )
    elif sig[2] != 0:
        # use Stachowiak's lemma 2 to find a Hamiltonian path in GE(Q|P[1])
        path = lemma2_extended_path([2] * sig[2])
        next_color = 3
    else:
        raise ValueError(
            "q = |Q| > 2 and GE(Q) has an even number of vertices is required for Lemma 11"
        )
    for ind, new_color in enumerate(sig[next_color:], start=next_color):
        cycle = _lemma10_helper(path, new_color, ind)
        path = cycle
    return path
