from connect_cycle_cover import get_connected_cycle_cover
from helper_operations.path_operations import adjacent
from helper_operations.permutation_graphs import stutterPermutations


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
    stutters = stutterPermutations(sig)
    if not stutters:
        return path
    # check if the path is a cycle
    if adjacent(path[0], path[-1]):
        # find the first node that is adjacent to a stutter
        for i, perm in enumerate(path):
            for stutter in stutters:
                if adjacent(perm, stutter):
                    # rotate the path so that the first node is the one that is adjacent to a stutter
                    path = path[i:] + path[:i]
                    break
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
    return result
