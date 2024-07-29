import argparse
from fractions import Fraction

from tqdm import tqdm

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
    transform_cross_edges,
    transform_cycle_cover,
)
from helper_operations.permutation_graphs import (
    extend_cycle_cover,
    get_perm_signature,
    multinomial,
    selectByTail,
    stutterPermutations,
    swapPair,
)
from stachowiak import lemma11
from verhoeff import HpathNS
from visualization import is_stutter_permutation


def merge_even_signatures(
    subsig: tuple[int, ...],
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
    cycle_cover_segments = generate_cycle_cover(subsig)
    tail_length = (
        2
        if all(n % 2 == 0 for n in subsig)
        else 1 if sum(n % 2 for n in subsig) == 1 else 0
    )
    if tail_length == 0:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {subsig} with {sum(n % 2 for n in subsig)} odd numbers."
        )
    # The cycles are split on the last elements
    end_tuple_order = generate_end_tuple_order(subsig)
    # while the depth of the list is more than 2, we need to connect the previous cycles
    single_cycle_cover = connect_recursive_cycles(cycle_cover_segments, subsig)
    cross_edges = find_cross_edges(subsig, single_cycle_cover)
    # The first cycle is a cycle
    # Ensure that the first cycle has start and end nodes that have the suffix _100
    tail = end_tuple_order[0]
    single_list = get_single_list(single_cycle_cover)
    start_cycles, end_cycles = split_sub_cycle_for_next_cross_edge(
        single_list, tail, cross_edges
    )
    # start_cycles, end_cycles = split_sub_cycle_for_next(single_list, tail)
    print(f"signature {subsig}")
    print(f"cut nodes 0: {start_cycles[-1]}, {end_cycles[0]}")
    for i, cycle_list in enumerate(single_cycle_cover[1:-1], start=1):
        temp_tail = swapPair(start_cycles[-1], -(tail_length + 1))[-(tail_length + 1) :]
        if temp_tail == (0, 1, 0):
            print(
                f"Loop All cross edges for {temp_tail}: {cross_edges.get((swapPair(temp_tail, 0), temp_tail))}"
            )
            tail122010 = selectByTail(cycle_list[0], (1, 2, 2) + temp_tail)
            tail212010 = selectByTail(cycle_list[0], (2, 1, 2) + temp_tail)
            print(
                f"cycle to cut tails {(1, 2, 2) + temp_tail}: {len(tail122010)} first: {tail122010[0]} index {cycle_list[0].index(tail122010[0])}"
            )
            print(
                f"subsequent nodes around this are: {cycle_list[0][cycle_list[0].index(tail122010[0]) - 1]}-{tail122010[0]}-{cycle_list[0][cycle_list[0].index(tail122010[0]) + 1]}"
            )
            print(
                f"cycle to cut tails {(2, 1, 2) + temp_tail}: {len(tail212010)} first: {tail212010[0]} index {cycle_list[0].index(tail212010[0])}"
            )
            print(
                f"subsequent nodes around this are: {cycle_list[0][cycle_list[0].index(tail212010[0]) - 1]}-{tail212010[0]}-{cycle_list[0][cycle_list[0].index(tail212010[0]) + 1]}"
            )
        cut_cycle = cut_sub_cycle_to_past(
            cycle_list[0],
            swapPair(start_cycles[-1], -(tail_length + 1)),
            swapPair(end_cycles[0], -(tail_length + 1)),
        )
        new_tail = end_tuple_order[i]
        # cycle_split = split_sub_cycle_for_next(cut_cycle, new_tail)
        cycle_split = split_sub_cycle_for_next_cross_edge(
            cut_cycle, new_tail, cross_edges
        )
        print(f"cut nodes {i}: {cycle_split[0][-1]}, {cycle_split[1][0]}")
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
    cycle_cover: list[list[tuple[int, ...]]], subsig: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    Connects the cycle cover to a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to connect, the depth of the list is undefined and depends on the cycle cover.
        subsig (tuple[int, ...]): The current signature, number of occurrences of each element.

    Returns:
        list[tuple[int, ...]]: The connected cycle cover
    """
    print(f"subsig: {subsig}")
    if len(cycle_cover) == 1:
        return cycle_cover[0]
    elif isinstance(cycle_cover[0][0], int):
        return cycle_cover
    # If there are multiple colors that occur an odd number of times
    if sum(n % 2 for n in subsig) > 1:
        # Use Stachowiak Lemma 11
        return []
    # If there is one color that occurs an odd number of times
    elif any(n % 2 == 1 for n in subsig):
        # Loop over the cycles in the cover and connect the cycle at index `i` ends with an element of color `i`
        return merge_even_signatures(subsig)
    elif all(n % 2 == 0 for n in subsig):
        # The cycles are split on the last two elements
        return merge_even_signatures(subsig)
    else:
        print(f"Not sure why this would happen, but happened for {subsig}")


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
            first_cycle_element = get_first_element(nested_cycle)
            last_element = first_cycle_element[-(tail_length):]

            # Get the new signature
            subsig = get_perm_signature(first_cycle_element[:-tail_length])
            sorted_subsig, subsig_transformer = get_transformer(subsig, lambda x: x[0])

            # if the sorted subsig is not the same as the subsig, we will just transform it into a sorted case and transform it back after
            shortened_cycle = None
            if sorted_subsig != subsig:
                shortened_cycle = generate_cycle_cover(sorted_subsig)
            else:
                shortened_cycle = shorten_cycle_cover(nested_cycle, last_element)
            connected_shortened = connect_cycle_cover(shortened_cycle, sorted_subsig)
            # Now we need to add the last element back to the connected shortened cycle
            if isinstance(connected_shortened[0], tuple):
                connected_shortened = [connected_shortened]
            # now transform the connected shortened subsig back to the original values
            transformed_short = transform_cycle_cover(
                connected_shortened, subsig_transformer
            )
            connected = extend_cycle_cover(transformed_short, last_element)
            single_cycle_cover.append(connected)
        else:
            single_cycle_cover.append(nested_cycle)
    return single_cycle_cover


@cache
def generate_end_tuple_order(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Generates the order of the end tuples of the cycles in the cycle cover.
    The end tuples are the tails of the cycles that are the nodes that connect them.
    They are cycles are ordered by their end tuples:\n
    - **All-even**: _00, _01/_10, _11, _12/_21, _22, , ...
    - **All-but-one-even**: _0, _1, _2, _3, _4, _5, ...

    Args:
        sig (tuple[int]): The signature of the permutation.

    Returns:
        list[tuple[int, ...]]:
            The order of the end tuples of the cycles in the cycle.
            These orders are as follows:\n
            - **All-even**: _100, _101, _211, _212,  ...\n
            The last tuple is of length 2. That is, the number of colors in the signature followed by the number of colors in the signature - 1.\n
            The first element is the change in the end tuple compared to the previous end tuple.\n
            - **All-but-one-even**: _10, _21, _32, _43, _54, _65, ...,  0S\n
            The last tuple starts with 0 and then S; the number of colors in the signature.\n
            The first element is the change in the end tuple compared to the previous end tuple.

    Raises:
        ValueError: If there is more than one change in consecutive end tuples.
        ValueError: If the signature is not all-even or all-but-one-even.
    """
    if len(list(sig)) <= 2:
        return []
    end_tuple_order = []
    sorted_sig, transformer = get_transformer(sig, lambda x: x[0])
    if sum(n % 2 for n in sig) == 1:
        # All-but-one-even signature
        for i, t in enumerate(transformer[:-1]):
            end_tuple_order.append((transformer[i + 1], t))
        end_tuple_order.append((transformer[0], transformer[-1]))
        return end_tuple_order
    elif all(n % 2 == 0 for n in sig):
        # All-even signature
        end_tuple_order = [(1, 0, 0), (1, 0, 1), (2, 1, 1)]
        for i in range(2, len(sorted_sig)-1):
            end_tuple_order.append((i, i - 1, i))
            end_tuple_order.append((0, i, i))
            for j in range(i - 2):
                end_tuple_order.append((j + 1, j, i))
            end_tuple_order.append((i + 1, i - 2, i))
        # The last row is reversed, from length-2 to 0
        end_tuple_order.append((len(sorted_sig) - 1, len(sorted_sig) - 2, len(sorted_sig) - 1))
        end_tuple_order.append((len(sorted_sig) - 3, len(sorted_sig) - 1, len(sorted_sig) - 1))
        for j in reversed(range(len(sorted_sig) - 3)):
            end_tuple_order.append((j, j + 1, len(sorted_sig) - 1))
        end_tuple_order.append((0, len(sorted_sig) - 1, 0))
        print(f"end tuple order: {end_tuple_order}")
        transformed_end_tuple_order = transform(end_tuple_order, transformer)
        return transformed_end_tuple_order
    else:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )


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
        start (tuple[int, ...]): The start node of the cycle.
        end (tuple[int, ...]): The end node of the cycle.

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


def split_sub_cycle_for_next_cross_edge(
    cycle_to_cut: list[tuple[int, ...]],
    tail: tuple[int, ...],
    cross_edges: dict[
        list[
            tuple[tuple[int, ...], tuple[int, ...]],
            tuple[tuple[int, ...], tuple[int, ...]],
        ]
    ],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Cuts the subcycle cover at nodes that end with `tail` and opens them such that the next cycle can be connected to the current cycle.
    The tail is the part of the permutation that should be at the end of the nodes.
    The cut is made based on a dictionary of cross edges that are used to connect the cycles.

    Args:
        cycle_to_cut (list[tuple[int, ...]]): The cycle to cut open at nodes with the provided tail. Both the node before and after the cut should end with `tail`.
        tail (tuple[int, ...]): The exact elements as a tuple of integers that the nodes should end with.
        cross_edges (dict[list[tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], tuple[int, ...]]]): The cross edges that connect the cycles.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]: The cycle cover cut open between the two nodes with the provided tail.

    Raises:
        ValueError: If the cross edge is not found in the cross edges dictionary.
    """
    next_tail = swapPair(tail, 0)
    cross_edge = cross_edges.get((tail, next_tail))[0][0]
    if cross_edge is None:
        raise ValueError(
            f"Cross edge {(tail, next_tail)} not found in cross edges {cross_edges}."
        )
    print(f"Tail {tail} gave cross nodes {cross_edge}")
    if tail == (1, 0, 0):
        print(f"All cross edges for {tail}: {cross_edges.get((tail, next_tail))}")
        tail122100 = selectByTail(cycle_to_cut, (1, 2, 2) + tail)
        tail212100 = selectByTail(cycle_to_cut, (2, 1, 2) + tail)
        print(
            f"cycle to cut tails {(1, 2, 2) + tail}: {len(tail122100)} first: {tail122100[0]} index {cycle_to_cut.index(tail122100[0])}"
        )
        print(
            f"subsequent nodes around this are: {cycle_to_cut[cycle_to_cut.index(tail122100[0]) - 1]}-{tail122100[0]}-{cycle_to_cut[(cycle_to_cut.index(tail122100[0]) + 1) % len(cycle_to_cut)]}"
        )
        print(
            f"cycle to cut tails {(2, 1, 2) + tail}: {len(tail212100)} first: {tail212100[0]} index {cycle_to_cut.index(tail212100[0])}"
        )
        print(
            f"subsequent nodes around this are: {cycle_to_cut[cycle_to_cut.index(tail212100[0]) - 1]}-{tail212100[0]}-{cycle_to_cut[(cycle_to_cut.index(tail212100[0]) + 1) % len(cycle_to_cut)]}"
        )
    print(
        f"index of cross edge: {cycle_to_cut.index(cross_edge[0])}, {cycle_to_cut.index(cross_edge[1])}"
    )
    if cycle_to_cut.index(cross_edge[0]) < cycle_to_cut.index(cross_edge[1]):
        return splitPathIn2(cycle_to_cut, cross_edge[0])
    else:
        return splitPathIn2(cycle_to_cut, cross_edge[1])


def get_connected_cycle_cover(sig: tuple[int]) -> list[tuple[int, ...]]:
    """
    Computes the a cycle on the non-stutter permutations for a given signature.
    If the signature is odd-2-1, the connected cycle cover is computed using lemma 11 by Stachowiak.
    Otherwise Verhoeff's cycle cover theorem is used to generate the cycle cover and that is then connected using the ``connect_cycle_cover`` function.

    Args:
        sig (tuple[int]): The signature for which the cycle on non-stutter permutations needs to be computed.

    Returns:
        list[tuple[int, ...]]: The connected cycle cover as a list of tuples, where each tuple represents a permutation.

    Raises:
        AssertionError: If the generated cycle cover by Verhoeff's theorem is empty.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
        - Stachowiak G. Hamilton Paths in Graphs of Linear Extensions for Unions of Posets. Technical report, 1992
    """
    if len(list(sig)) == 0:
        return []
    sorted_sig, transformer = get_transformer(sig, lambda x: [x[0] % 2, x[0]])
    if sig != sorted_sig:
        return transform(get_connected_cycle_cover(sorted_sig), transformer)
    if len(list(sig)) == 2 and any(c % 2 == 0 for c in sig):
        return HpathNS(sig[0], sig[1])
    # if sig contains a 1, a 2 and an odd number, we need to compute separately
    if len(list(sig)) < 3 or (sig[0] % 2 == 1 and sig[1] == 1 and sig[2] == 2):
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
    sig: tuple[int],
    cycle_cover: list[tuple[int, ...]],
) -> dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    """
    Find parallel edges in the cycle cover. These edges are pairs of nodes in the cycle cover that have a tail that connects them to the next cycle.
    The tail is defined by the number of odd colors in the signature.

    Args:
        sig (tuple[int]): The signature of the permutation.
        cycle_cover (list[tuple[int, ...]]): The cycle cover to find parallel edges in.

    Returns:
        dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
            A dictionary where the key is the pair of tails of the cycle that are combined and the value is the list of parallel edges.
            Each parallel edge is a tuple of two tuples of permutations (a permutation is a tuple of integers).
    """
    if len(list(sig)) == 0:
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
    tails = generate_end_tuple_order(sig)
    # generate the start tuples by swapping the first two elements of the tails
    start_tails = [swapPair(tail, 0) for tail in tails]
    if len(cycle_cover) == 1:
        return {
            (tails[0]): [filter_adjacent_edges_by_tail(cycle_cover[0], tails[0])],
            (start_tails[0]): [
                filter_adjacent_edges_by_tail(cycle_cover[0], start_tails[0])
            ],
        }
    parallel_edges = {}
    for i, cycle in enumerate(cycle_cover[:-1]):
        parallel_edges[tails[i]] = filter_adjacent_edges_by_tail(cycle[0], tails[i])
        parallel_edges[start_tails[i]] = filter_adjacent_edges_by_tail(
            cycle_cover[i + 1][0],
            start_tails[i],
        )
    parallel_edges[tails[-1]] = filter_adjacent_edges_by_tail(
        cycle_cover[-1][0],
        tails[-1],
    )
    parallel_edges[start_tails[-1]] = filter_adjacent_edges_by_tail(
        cycle_cover[0][0],
        start_tails[-1],
    )
    return parallel_edges


def find_cross_edges(
    sig: tuple[int],
    cycle_cover: list[tuple[int, ...]],
) -> dict[
    list[
        tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], tuple[int, ...]]
    ]
]:
    """
    Find the cross edges in the cycle cover. These are pairs of parallel edges between cycles that are adjacent.
    The cross edges are used to connect the cycles in the cycle cover.

    Args:
        sig (tuple[int]): The signature of the permutation.
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
    common_cross_edges_to_equal = []
    common_cross_edges_from_equal = []
    common_cross_edges_different = []
    for tail1, parallel_edges1 in parallel_edges.items():
        tail2 = swapPair(tail1, 0)
        if (tail1, tail2) in cross_edges or (tail2, tail1) in cross_edges:
            continue
        print(f"tail1: {tail1}, tail2: {tail2}")
        parallel_edges2 = parallel_edges[tail2]
        for edge1_index in tqdm(range(len(parallel_edges1))):
            edge1 = parallel_edges1[edge1_index]
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
        if (tail1, tail2) in cross_edges:
            cross_edge_sig = get_perm_signature(
                cross_edges[(tail1, tail2)][0][0][0][: -len(tail1) + 1]
            )
            total_edges = multinomial(cross_edge_sig)
            print(
                f"Cross edge {(tail1, tail2)} has a ratio of {len(cross_edges[(tail1, tail2)])}/{total_edges} = "
                f"{Fraction(len(cross_edges[(tail1, tail2)]), total_edges).numerator}/{Fraction(len(cross_edges[(tail1, tail2)]), total_edges).denominator}"
            )
            if len(tail1) == 3:
                if tail1 == (1, 0, 0):
                    common_cross_edges_from_equal = cross_edges[(tail1, tail2)]
                elif tail2 == (0, 1, 1):
                    common_cross_edges_to_equal = cross_edges[(tail1, tail2)]
                elif (tail1, tail2) == ((3, 0, 2), (0, 3, 2)):
                    common_cross_edges_different = cross_edges[(tail1, tail2)]
                elif tail1[1] != tail1[2] and tail2[1] != tail2[2]:
                    transformer = []
                    for i in range(len(sig)):
                        if i == tail1[0]:
                            transformer.append(3)
                        elif i == tail1[1]:
                            transformer.append(0)
                        elif i == tail1[2]:
                            transformer.append(2)
                        else:
                            transformer.append(i)
                    changed_indices = [
                        t if t != i else -1 for i, t in enumerate(transformer)
                    ]
                    for ind, changed_index in enumerate(changed_indices):
                        if changed_index != -1 and changed_indices[changed_index] == -1:
                            transformer[changed_index] = ind
                    transformed_cross_edges = transform_cross_edges(
                        cross_edges[(tail1, tail2)], transformer
                    )
                    for common in common_cross_edges_different:
                        if common not in transformed_cross_edges:
                            common_cross_edges_different.remove(common)
                elif tail1[1] == tail1[2]:
                    # create transformer list; going from 0 to n-1 but if i is 0 then it should be tail1[1] and vice versa
                    transformer = []
                    for i in range(len(sig)):
                        if i == tail1[0]:
                            transformer.append(1)
                        elif i == tail1[1]:
                            transformer.append(0)
                        elif i == 0 and tail1[1] == 1:
                            transformer.append(tail1[0])
                        elif i == 0:
                            transformer.append(tail1[1])
                        elif i == 1 and tail1[0] == 0:
                            transformer.append(tail1[1])
                        elif i == 1:
                            transformer.append(tail1[0])
                        else:
                            transformer.append(i)
                    transformed_cross_edges = transform_cross_edges(
                        cross_edges[(tail1, tail2)], transformer
                    )
                    for common in common_cross_edges_from_equal:
                        if common not in transformed_cross_edges:
                            common_cross_edges_from_equal.remove(common)
                elif tail2[1] == tail2[2]:
                    transformer = []
                    for i in range(len(sig)):
                        if i == tail2[1]:
                            transformer.append(1)
                        elif i == tail2[0]:
                            transformer.append(0)
                        elif i == 0 and tail2[1] == 1:
                            transformer.append(tail2[0])
                        elif i == 0:
                            transformer.append(tail2[1])
                        elif i == 1 and tail2[0] == 0:
                            transformer.append(tail2[1])
                        elif i == 1:
                            transformer.append(tail2[0])
                        else:
                            transformer.append(i)
                    transformed_cross_edges = transform_cross_edges(
                        cross_edges[(tail1, tail2)], transformer
                    )
                    for common in common_cross_edges_to_equal:
                        if common not in transformed_cross_edges:
                            common_cross_edges_to_equal.remove(common)
    # reverse common cross edges to equal
    print(f"common cross edges to equal: {common_cross_edges_to_equal}")
    common_cross_edges_to_equal = [edge[::-1] for edge in common_cross_edges_to_equal]
    equalize_transformer = [
        0 if i == 1 else 1 if i == 0 else i for i in range(len(sig))
    ]
    from_to_equal = transform_cross_edges(
        common_cross_edges_to_equal, equalize_transformer
    )
    for common in from_to_equal:
        if common not in common_cross_edges_from_equal:
            from_to_equal.remove(common)
    print(f"common cross edges from equal: {common_cross_edges_from_equal}")
    print(f"common cross edges from_to_equal {sig}: {from_to_equal}")
    print(f"common cross edges different {sig}: {common_cross_edges_different}")
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
    sig = tuple([int(x) for x in args.signature.split(",")])
    connected_cycle_cover = get_connected_cycle_cover(sig)
    if args.verbose:
        print(f"Connected cycle cover: {connected_cycle_cover}")
    stut_count = len(stutterPermutations(sig))
    print(
        f"Cycle cover is a cycle {cycleQ(connected_cycle_cover)} and a path {pathQ(connected_cycle_cover)} "
        f"with {len(connected_cycle_cover)}/{multinomial(sig)} (incl {stut_count} stutters is {stut_count+len(connected_cycle_cover)}) permutations."
    )
