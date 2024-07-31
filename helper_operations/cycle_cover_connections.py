from fractions import Fraction

from tqdm import tqdm

from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    get_transformer,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import (
    get_perm_signature,
    multinomial,
    swapPair,
)


def get_tail_length(sig: tuple[int]) -> int:
    """
    Get the length of the tail to cut the cycle cover on.

    Args:
        sig (tuple[int]): The signature of the permutation.

    Returns:
        int: The length of the tail.

    Raises:
        ValueError: If the signature is not all-even or all-but-one-even.
    """
    if all(n % 2 == 0 for n in sig):
        return 2
    elif sum(n % 2 for n in sig) == 1:
        return 1
    else:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )


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
    if sum(n % 2 for n in sig) == 1 or sum(n % 2 for n in sig) > 2:
        # All-but-one-even signature
        for i, t in enumerate(transformer[:-1]):
            end_tuple_order.append((transformer[i + 1], t))
        end_tuple_order.append((transformer[0], transformer[-1]))
        return end_tuple_order
    elif all(n % 2 == 0 for n in sig):
        # All-even signature
        end_tuple_order = [(1, 0, 0), (1, 0, 1), (2, 1, 1)]
        for i in range(2, len(sorted_sig) - 1):
            end_tuple_order.append((i, i - 1, i))
            end_tuple_order.append((0, i, i))
            for j in range(i - 2):
                end_tuple_order.append((j + 1, j, i))
            end_tuple_order.append((i + 1, i - 2, i))
        # The last row is reversed, from length-2 to 0
        end_tuple_order.append(
            (len(sorted_sig) - 1, len(sorted_sig) - 2, len(sorted_sig) - 1)
        )
        end_tuple_order.append(
            (len(sorted_sig) - 3, len(sorted_sig) - 1, len(sorted_sig) - 1)
        )
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
    tuple[int, ...],
    list[
        tuple[
            tuple[tuple[int, ...], tuple[int, ...]],
            tuple[tuple[int, ...], tuple[int, ...]],
        ],
    ],
]:
    """
    Find the cross edges in the cycle cover. These are pairs of parallel edges between cycles that are adjacent.
    The cross edges are used to connect the cycles in the cycle cover.

    Args:
        sig (tuple[int]): The signature of the permutation.
        cycle_cover (list[tuple[int, ...]]): The cycle cover to find cross edges in.

    Returns:
        dict[tuple[int, ...], list[tuple[tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], tuple[int, ...]]]]]:
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
        if (tail1, tail2) in cross_edges or (tail2, tail1) in cross_edges:
            continue
        print(f"tail1: {tail1}, tail2: {tail2}")
        parallel_edges2 = parallel_edges[tail2]
        for edge1_index in tqdm(range(len(parallel_edges1))):
            edge1 = parallel_edges1[edge1_index]
            cross = None
            for edge2 in parallel_edges2:
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
                    # if an edge is adjacent to one parallel edge, it cannot be adjacent to another from that same cycle
                    break
            if cross is not None:
                continue
        if (tail1, tail2) in cross_edges:
            cross_edge_sig = get_perm_signature(
                cross_edges[(tail1, tail2)][0][0][0][: -len(tail1) + 1]
            )
            total_edges = multinomial(cross_edge_sig)
            print(
                f"Cross edge {(tail1, tail2)} has a ratio of {len(cross_edges[(tail1, tail2)])}/{total_edges} = "
                f"{Fraction(len(cross_edges[(tail1, tail2)]), total_edges).numerator}/{Fraction(len(cross_edges[(tail1, tail2)]), total_edges).denominator}"
            )
    return cross_edges


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
    print(
        f"index of cross edge: {cycle_to_cut.index(cross_edge[0])}, {cycle_to_cut.index(cross_edge[1])}"
    )
    if cycle_to_cut.index(cross_edge[0]) < cycle_to_cut.index(cross_edge[1]):
        return splitPathIn2(cycle_to_cut, cross_edge[0])
    else:
        return splitPathIn2(cycle_to_cut, cross_edge[1])
