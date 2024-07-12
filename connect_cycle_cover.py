import argparse
import collections

from cycle_cover import generate_cycle_cover
from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    cycleQ,
    get_first_element,
    get_single_list,
    get_transformer,
    pathQ,
    shorten_cycle_cover,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import (
    extend_cycle_cover,
    selectByTail,
    swapPair,
)
from stachowiak import lemma11
from verhoeff import HpathNS
from visualization import is_stutter_permutation


def merge_even_signatures(
    cycle_cover_segments: list[list[tuple[int, ...]]],
    sig: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """
    Merges the cycles in the cycle cover for all-even and all-but-one-even permutations.
    The cycles are connected to form a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.
    This is done by looking at the suffix of the cycles and connecting them to the next cycle. The suffix is the last `tail_length` elements of the cycle:\n
    - 1 for all-but-one-even permutations
    - 2 for all-even permutations
    The cycles are split on the last elements and connected to the next cycle.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to merge.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list[tuple[int, ...]]: The merged cycle cover
    """
    tail_length = (
        2 if all(n % 2 == 0 for n in sig) else 1 if sum(n % 2 for n in sig) == 1 else 0
    )
    if tail_length == 0:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )
    # while the depth of the list is more than 2, we need to connect the previous cycles
    single_cycle_cover = connect_recursive_cycles(cycle_cover_segments, sig)
    
    cross_edges = find_cross_edges(sig, single_cycle_cover)
    print(f"Cross edges sig {sig}: {{\n" + "\n".join("{!r}: {!r},".format(k, v) for k, v in cross_edges.items()) + "\n }")
    # The cycles are split on the last elements
    end_tuple_order = generate_end_tuple_order(sig, single_cycle_cover)
    print(f"End tuple order: {end_tuple_order} for signature {sig}")
    # The first cycle is a cycle
    # Ensure that the first cycle has start and end nodes that have the suffix _100
    tail = end_tuple_order[0]
    single_list = get_single_list(single_cycle_cover)
    start_cycles, end_cycles = split_sub_cycle_for_next(single_list, tail)
    print(f"cut nodes 0: {start_cycles[-1]}, {end_cycles[0]}")
    for i, cycle_list in enumerate(single_cycle_cover[1:-1], start=1):
        cut_cycle = cut_sub_cycle_to_past(
            cycle_list[0],
            swapPair(start_cycles[-1], -(tail_length + 1)),
            swapPair(end_cycles[0], -(tail_length + 1)),
        )
        new_tail = end_tuple_order[i]
        cycle_split = split_sub_cycle_for_next(cut_cycle, new_tail)
        start_cycles += cycle_split[0]
        end_cycles = cycle_split[1] + end_cycles

    # The last cycle is a cycle and has to be pasted to the past one but not cut in itself
    cut_cycle = cut_sub_cycle_to_past(
        single_cycle_cover[-1][0],
        swapPair(start_cycles[-1], -(tail_length + 1)),
        swapPair(end_cycles[0], -(tail_length + 1)),
    )
    start_cycles += cut_cycle
    return start_cycles + end_cycles


def connect_cycle_cover(
    cycle_cover: list[list[tuple[int, ...]]], sig: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    Connects the cycle cover to a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to connect, the depth of the list is undefined and depends on the cycle cover.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list[tuple[int, ...]]: The connected cycle cover
    """
    if len(cycle_cover) == 1:
        return cycle_cover[0]
    elif isinstance(cycle_cover[0][0], int):
        return cycle_cover
    # If there is one color that occurs an odd number of times
    elif any(n % 2 == 1 for n in sig):
        # Loop over the cycles in the cover and connect the cycle at index `i` ends with an element of color `i`
        return merge_even_signatures(cycle_cover, sig)
    elif all(n % 2 == 0 for n in sig):
        # The cycles are split on the last two elements
        return merge_even_signatures(cycle_cover, sig)
    else:
        print(f"Not sure why this would happen, but happened for {sig}")


def connect_recursive_cycles(
    cycle_cover: list[list[tuple[int, ...]]], sig: tuple[int, ...]
) -> list[list[tuple[int, ...]]]:
    """
    Recursively connects the cycles in the cycle cover to form a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.
    The cycles are connected by looking at the suffix of the cycles and connecting them to the next cycle.
    The suffix is the last `tail_length` elements of the cycle:\n
    - 1 for all-but-one-even permutations
    - 2 for all-even permutations
    This is the inductive step of the connection of the cycles.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to connect.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list[list[tuple[int, ...]]]: The connected cycle cover.
    """
    tail_length = (
        2 if all(n % 2 == 0 for n in sig) else 1 if sum(n % 2 for n in sig) == 1 else 0
    )
    if tail_length == 0:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )
    single_cycle_cover = []
    for nested_cycle in cycle_cover:
        if (
            isinstance(nested_cycle, list)
            and isinstance(nested_cycle[0], list)
            and isinstance(nested_cycle[0][0], list)
        ):
            # we need to remove the last element from every list in the nested cycle to connect them
            last_element = get_first_element(nested_cycle)[-(tail_length):]
            shortened_cycle = shorten_cycle_cover(nested_cycle, last_element)
            # For every element in last_element, we need to subtract 1 from the corresponding element in the signature
            subsig = tuple(
                (
                    val - collections.Counter(last_element)[idx]
                    if idx in last_element
                    else val
                )
                for idx, val in enumerate(list(sig))
            )
            connected_shortened = connect_cycle_cover(shortened_cycle, subsig)
            # Now we need to add the last element back to the connected shortened cycle
            if isinstance(connected_shortened[0], tuple):
                connected_shortened = [connected_shortened]
            connected = extend_cycle_cover(connected_shortened, last_element)
            single_cycle_cover.append(connected)
        else:
            single_cycle_cover.append(nested_cycle)
    return single_cycle_cover


def generate_end_tuple_order(
    sig: list[int], cycle_cover: list[list[tuple[int, ...]]]
) -> list[tuple[int, ...]]:
    """
    Generates the order of the end tuples of the cycles in the cycle cover.
    The end tuples are the last `tail_length` elements of the cycle.
    The tail
    They are cycles are ordered by their end tuples:\n
    - **All-even**: _00, _01/_10, _11, _12/_21, _22, _02/_20, _23/_32, _33, _03/_30, _31/_13, _34/_43, _44, _04/_40, _41/_14, _42/_24, ...
    - **All-but-one-even**: _0, _1, _2, _3, _4, _5, ...

    Args:
        sig (list[int]): The signature of the permutation.
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to generate the end tuple order for.

    Returns:
        list[tuple[int, ...]]:
            The order of the end tuples of the cycles in the cycle.
            These orders are as follows:\n
            - **All-even**: _100, _101, _211, _212, _022, _302, _323, _033, _103, _413, _443, _44, _404, _414, _424, ...\n
            The last tuple is of length 2. That is, the number of colors in the signature followed by the number of colors in the signature - 1.\n
            The first element is the change in the end tuple compared to the previous end tuple.\n
            - **All-but-one-even**: _10, _21, _32, _43, _54, _65, ...
            The last tuple is of length 1. That is, the number of colors in the signature.\n
            The first element is the change in the end tuple compared to the previous end tuple.

    Raises:
        ValueError: If there is more than one change in consecutive end tuples.
        ValueError: If the tail length is not 1 or 2, i.e. the signature is not all-even or all-but-one-even.
    """
    if len(cycle_cover) == 0:
        return []
    tail_length = (
        2 if all(n % 2 == 0 for n in sig) else 1 if sum(n % 2 for n in sig) == 1 else 0
    )
    if tail_length == 0:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )
    end_tuple_order = []
    for c in cycle_cover:
        end_tuple_order.append(get_first_element(c)[-tail_length:])
    for i in range(len(end_tuple_order) - 1):
        # Now prepend to every end_tuple the element that is different in the next end_tuple
        # find the duplicates in the end tuple
        dups = [
            item
            for item, count in collections.Counter(end_tuple_order[i + 1]).items()
            if count > 1
        ]
        if len(dups) > 0:
            changes = tuple(dups)
        else:
            changes = tuple(
                end_tuple_order[i + 1][j]
                for j in range(len(end_tuple_order[i]))
                if not end_tuple_order[i + 1][j] in end_tuple_order[i]
            )
        print(
            f"changes: {changes}, end_tuple_order[i]: {end_tuple_order[i]}, dups: {dups}"
        )
        if len(changes) != 1:
            raise ValueError(
                f"There should be only one change in the end tuple order: {changes} + {end_tuple_order[i]}"
            )
        # make sure that the change number is different from the first number in end_tuple_order[i]
        if changes[0] != end_tuple_order[i][0]:
            end_tuple_order[i] = changes + end_tuple_order[i]
        else:
            end_tuple_order[i] = changes + end_tuple_order[i][::-1]
    return end_tuple_order


def cut_sub_cycle_to_past(
    cycle_to_cut: list[tuple[int, ...]],
    start: tuple[int, ...],
    end: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """
    Opens the cycle such that the previous cycle can be connected to the current cycle.
    The start and end nodes are the nodes that should be at the start and end of the cycle.

    Args:
        cycle_to_cut (list[tuple[int, ...]]): The cycle to cut.
        start (tuple[int, ...]): The start nodes of the cycle.
        end (tuple[int, ...]): The end nodes of the cycle.

    Returns:
        list[tuple[int, ...]]: The cut cycle.

    Raises:
        AssertionError: If the start or end nodes are not found in the cycle.
        ValueError: If the start and end nodes are not adjacent in the cycle.
    """
    cut_cycle = cutCycle(cycle_to_cut, start)
    assert end in cut_cycle
    if cut_cycle[-1] == end:
        return cut_cycle
    elif cut_cycle[1] == end:
        return cut_cycle[:1] + cut_cycle[1:][::-1]
    else:
        raise ValueError(
            f"Start and end nodes {start} and {end} are not adjacent in the cycle.\n"
            f"Start node at index {cut_cycle.index(start)} and end node at index {cut_cycle.index(end)}.\n"
            f"Adjacent nodes to start index: {cut_cycle[cut_cycle.index(start) - 1]}-{cut_cycle[cut_cycle.index(start)]}-{cut_cycle[cut_cycle.index(start) + 1]}.\n"
            f"Adjacent nodes to end index: {cut_cycle[cut_cycle.index(end) - 1]}-{cut_cycle[cut_cycle.index(end)]}-{cut_cycle[cut_cycle.index(end) + 1]}."
        )


def split_sub_cycle_for_next(
    cycle_to_cut: list[tuple[int, ...]], tail: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Cuts the subcycle cover at nodes that end with `tail` and opens them such that the next cycle can be connected to the current cycle.
    The tail is the part of the permutation that should be at the end of the nodes.
    The first two nodes of the tail are swapped to ensure they are not forming stutter permutations.

    Args:
        cycle_to_cut (list[tuple[int, ...]]): The cycle to cut open at nodes with the provided tail. Both the node before and after the cut should end with `tail`.
        tail (tuple[int, ...]): The exact elements as a tuple of integers that the nodes should end with.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]: The cycle cover cut open between the two nodes with the provided tail.

    Raises:
        ValueError: If not enough tail nodes are found in the first cycle (i.e. less than 2).
        ValueError: If no valid tail nodes are found.
    """
    tail_nodes = selectByTail(cycle_to_cut, tail)
    if len(tail_nodes) < 2:
        print(f"Cycle to cut: {cycle_to_cut}, tail: {tail}")
        raise ValueError(
            f"Not enough tail nodes found in the first cycle: {tail_nodes}. The tail was {tail}."
        )
    tail_idx = 0
    # Now check if swapping the first two elements of the tail nodes gives a stutter permutation
    # Also check whether the nodes are adjacent within the cycle
    while (
        is_stutter_permutation(swapPair(tail_nodes[tail_idx], -len(tail)))
        or is_stutter_permutation(swapPair(tail_nodes[tail_idx + 1], -len(tail)))
        or not adjacent(tail_nodes[tail_idx], tail_nodes[tail_idx + 1])
        or not abs(
            cycle_to_cut.index(tail_nodes[tail_idx])
            - cycle_to_cut.index(tail_nodes[tail_idx + 1])
        )
        == 1
    ):
        tail_idx += 1
        if tail_idx == len(tail_nodes) - 1:
            # manually check the last-first combination
            if (
                is_stutter_permutation(swapPair(tail_nodes[-1], -len(tail)))
                or is_stutter_permutation(swapPair(tail_nodes[0], -len(tail)))
                or not adjacent(tail_nodes[-1], tail_nodes[0])
                or not abs(
                    cycle_to_cut.index(tail_nodes[-1])
                    - cycle_to_cut.index(tail_nodes[0])
                )
                == 1
            ):
                raise ValueError(f"No valid tail nodes found: {tail_nodes}")
            else:
                break
    return splitPathIn2(cycle_to_cut, tail_nodes[tail_idx])


def get_connected_cycle_cover(sig: list[int]) -> list[tuple[int, ...]]:
    """
    Computes the a cycle on the non-stutter permutations for a given signature.
    If the signature is odd-2-1, the connected cycle cover is computed using lemma 11 by Stachowiak.
    Otherwise Verhoeff's cycle cover theorem is used to generate the cycle cover and that is then connected using the ``connect_cycle_cover`` function.

    Args:
        sig (list[int]): The signature for which the cycle on non-stutter permutations needs to be computed.

    Returns:
        list[tuple[int, ...]]: The connected cycle cover as a list of tuples, where each tuple represents a permutation.

    Raises:
        AssertionError: If the generated cycle cover by Verhoeff's theorem is empty.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
    """
    if len(sig) == 0:
        return []
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])
    if sig != sorted_sig:
        return transform(get_connected_cycle_cover(sorted_sig), transformer)
    if len(sig) == 2 and any(c % 2 == 0 for c in sig):
        return HpathNS(sig[0], sig[1])
    # if sig contains a 1, a 2 and an odd number, we need to compute separately
    if len(sig) < 3 or (sig[0] % 2 == 1 and sig[1] == 1 and sig[2] == 2):
        return lemma11(sig)
    else:
        cover = generate_cycle_cover(sig)
        assert len(cover) > 0
        return connect_cycle_cover(cover, sig)


def filter_adjacent_edges_by_tail(
    cycle: list[tuple[int, ...]],
    tail: tuple[int, ...],
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """
    From a cycle, get all the edges (i.e. the pairs of consecutive permutations).
    Then filter those edges such that both nodes have the specified tail.

    Args:
        cycle (list[tuple[int, ...]]): The cycle to filter.
        tail (tuple[int, ...]): The tail that the nodes should have.

    Returns:
        list[tuple[tuple[int, ...], tuple[int, ...]]]: The edges that have the specified tail.
    """
    edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
    # if the list is a cycle, also add that edge
    if adjacent(cycle[-1], cycle[0]):
        edges.append((cycle[-1], cycle[0]))
    filtered_edges = [
        (edge[0], edge[1])
        for edge in edges
        if edge[0][-len(tail) :] == tail and edge[1][-len(tail) :] == tail
    ]
    return filtered_edges


def find_parallel_edges_in_cycle_cover(
    sig: list[int],
    cycle_cover: list[tuple[int, ...]],
) -> dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    """
    Find parallel edges in the cycle cover. These edges are pairs of nodes in the cycle cover that have a tail that connects them to the next cycle.
    The tail is defined by the number of odd colors in the signature.

    Args:
        sig (list[int]): The signature of the permutation.
        cycle_cover (list[tuple[int, ...]]): The cycle cover to find parallel edges in.

    Returns:
        dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
            A dictionary where the key is the pair of tails of the cycle that are combined and the value is the list of parallel edges.
            Each parallel edge is a tuple of two tuples of permutations (a permutation is a tuple of integers).
    """
    if len(sig) == 0:
        raise ValueError("Signature should contain at least one element")
    if any(c < 0 for c in sig):
        raise ValueError("Signature should contain only positive integers")
    if len(cycle_cover) == 0:
        return []
    tail_length = (
        2 if all(n % 2 == 0 for n in sig) else 1 if sum(n % 2 for n in sig) == 1 else 0
    )
    if tail_length == 0:
        # this is stachowiak's case, this already is a cycle
        return []
    tails = generate_end_tuple_order(sig, cycle_cover)
    # generate the start tuples by swapping the first two elements of the tails
    print(f"tails: {tails}")
    start_tails = [swapPair(tail, 0) for tail in tails]
    if len(cycle_cover) == 1:
        return {
            (tails[0]): [filter_adjacent_edges_by_tail(cycle_cover[0], tails[0])],
            (start_tails[0]): [filter_adjacent_edges_by_tail(cycle_cover[0], start_tails[0])],
        }
    parallel_edges = {}
    for i, cycle in enumerate(cycle_cover[:-1]):
        parallel_edges[tails[i]] = filter_adjacent_edges_by_tail(cycle[0], tails[i])
        parallel_edges[start_tails[i]] = filter_adjacent_edges_by_tail(cycle_cover[i + 1][0], start_tails[i])
    return parallel_edges



def find_cross_edges(
    sig: list[int],
    cycle_cover: list[tuple[int, ...]],
) -> dict[list[tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], tuple[int, ...]]]]:
    """
    Find the cross edges in the cycle cover. These are pairs of parallel edges between cycles that are adjacent.
    The cross edges are used to connect the cycles in the cycle cover.

    Args:
        sig (list[int]): The signature of the permutation.
        cycle_cover (list[tuple[int, ...]]): The cycle cover to find cross edges in.

    Returns:
        dict[tuple[int, ...], list[tuple[tuple[int, ...], tuple[int, ...]]]]:
            A dictionary where the key is a pair of tails of the cycle that are combined and the value is the list of cross edges.
            Each cross edge is a tuple of two tuples of permutations (a permutation is a tuple of integers).

    Raises:
        ValueError: If the cycle cover is empty.
    """
    if len(cycle_cover) == 0:
        raise ValueError("Cycle cover should contain at least one cycle.")
    parallel_edges = find_parallel_edges_in_cycle_cover(sig, cycle_cover)
    if len(parallel_edges) < 2:
        return []
    if len(parallel_edges) == 2:
        return {
            (list(parallel_edges.keys())[0], list(parallel_edges.keys())[1]): [
                (edge1, edge2)
                for edge1 in parallel_edges[list(parallel_edges.keys())[0]]
                for edge2 in parallel_edges[list(parallel_edges.keys())[1]]
            ]
        }
    cross_edges = {}
    for tail1, parallel_edges1 in parallel_edges.items():
        tail2 = swapPair(tail1, 0)
        parallel_edges2 = parallel_edges[tail2]
        for edge1 in parallel_edges1:
            for edge2 in parallel_edges2:
                cross = None
                if adjacent(edge1[0], edge2[0]) and adjacent(edge1[1], edge2[1]):
                    cross = (edge1, edge2)
                elif adjacent(edge1[0], edge2[1]) and adjacent(edge1[1], edge2[0]):
                    cross = (edge1, edge2[::-1])
                elif adjacent(edge1[1], edge2[0]) and adjacent(edge1[0], edge2[1]):
                    cross = (edge1[::-1], edge2)
                if cross is not None:
                    if (tail1, tail2) in cross_edges:
                        cross_edges[(tail1, tail2)].append(cross)
                    else:
                        cross_edges[(tail1, tail2)] = [cross]
    return cross_edges


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
    sig = [int(x) for x in args.signature.split(",")]
    connected_cycle_cover = get_connected_cycle_cover(sig)
    if args.verbose:
        print(f"Connected cycle cover: {connected_cycle_cover}")
    print(
        f"Cycle cover is a cycle {cycleQ(connected_cycle_cover)} and a path {pathQ(connected_cycle_cover)}"
    )
