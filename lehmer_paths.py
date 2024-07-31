import argparse

from connect_cycle_cover import get_connected_cycle_cover
from helper_operations.path_operations import adjacent, cycleQ, pathQ
from helper_operations.permutation_graphs import (
    HcycleQ,
    HpathQ,
    multinomial,
    stutterPermutations,
)


def order_path_to_stutter_start(
    path: list[tuple[int]], stutters: list[tuple[int, ...]]
) -> list[tuple[int, ...]]:
    """
    If the path is a cycle; order the cycle to make the start node adjacent to a stutter.
    If the path is not a cycle; just return the original path.

    Args:
        path (list[tuple[int]]): The path to order.
        stutters (list[tuple[int, ...]]): The stutters to incorporate.

    Returns:
        list[tuple[int, ...]]: The ordered path.
    """
    # check if the path is a cycle
    if adjacent(path[0], path[-1]):
        # find the first node that is adjacent to a stutter
        for i, perm in enumerate(path):
            for stutter in stutters:
                if adjacent(perm, stutter):
                    # rotate the path so that the first node is the one that is adjacent to a stutter
                    return path[i:] + path[:i]
    return path


def incorporate_stutters(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Creates a cycle/path on the non-stutter permutations and then incorporates the stutters to create a Lehmer cycle/path.
    See the Notes for which signatures result in a path instead of a cycle.

    Args:
        sig (tuple[int]): The input signature.

    Returns:
        list[tuple[int, ...]]: The list of tuples representing the valid cycle/path on non-stutter permutations with the stutters incorporated.

    Note:
        Some signatures do not result in a cycle but in a path, the signatures that result in a path are:\n
        - Even-1 or odd-1 *(Linear neighbor-swap graphs)*
        - Odd-odd
        - Odd-even / even-odd
        - Even-1-1
    """
    path = get_connected_cycle_cover(sig)
    # the \033[1m makes the text bold and the \033[91m makes the text red
    non_stutter_cycle = "\033[1m\033[91m Neither a valid Hamiltonian cycle nor Hamiltonian path\033[0m\033[0m"
    if HcycleQ(path, sig):
        # the \033[92m makes the text green
        non_stutter_cycle = "\033[1m\033[92m A valid Hamiltonian cycle\033[0m\033[0m"
    elif HpathQ(path, sig):
        # the \033[94m makes the text blue
        non_stutter_cycle = "\033[1m\033[94m A valid Hamiltonian path\033[0m\033[0m"
    elif len(path) == 0 and len(stutterPermutations(sig)) > 0:
        return (
            stutterPermutations(sig),
            "\033[1m\033[91m Only stutter permutations were found\033[0m\033[0m",
        )
    else:
        raise ValueError(
            "The connected cycle cover does not result in a Hamiltonian path."
        )
    print(f"The non-stutter permutations gave:{non_stutter_cycle}.")
    stutters = stutterPermutations(sig)
    print(f"There were {len(stutters)} stutters. {stutters} with signature {sig}.")
    if not stutters:
        return path, non_stutter_cycle
    path = order_path_to_stutter_start(path, stutters)
    result = []
    for i, perm in enumerate(path):
        adj = False
        for stutter in stutters:
            if adjacent(perm, stutter):
                adj = True
                if i != 0:
                    result.append(perm)
                result.append(stutter)
                stutters.remove(stutter)
        if not (adj and i == len(path) - 1):
            result.append(perm)
    return result, non_stutter_cycle


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
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    args = parser.parse_args()
    sig = tuple([int(x) for x in args.signature.split(",")])
    result, without_stutter_cycle = incorporate_stutters(sig)
    if args.verbose:
        print(f"Lehmer path: {result}")
    # the \033[1m makes the text bold and the \033[91m makes the text red
    lehmer_path = (
        "\033[1m\033[91m neither a valid Lehmer cycle nor Lehmer path\033[0m\033[0m"
    )
    if cycleQ(result):
        # the \033[92m makes the text green
        lehmer_path = "\033[1m\033[92m a valid Lehmer cycle\033[0m\033[0m"
    elif pathQ(result):
        # the \033[94m makes the text blue
        lehmer_path = "\033[1m\033[94m a valid Lehmer path\033[0m\033[0m"
    print(f"Input signature: {sig} gave{lehmer_path}")
    print(
        f"There were {len(result)} permutations in the cycle/path. Which results in a defect of "
        f"{len(result)}-{multinomial(sig)}={len(result)-multinomial(sig)} since there were {len(stutterPermutations(sig))} stutters."
        f"The non-stutter permutations gave:{without_stutter_cycle}."
    )
