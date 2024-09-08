import bisect
import csv
import os
from ast import literal_eval
from fractions import Fraction
from functools import cache

from tqdm import tqdm

from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    get_first_element,
    get_transformer,
    splitPathIn2,
    transform,
)
from helper_operations.permutation_graphs import (
    get_perm_signature,
    multinomial,
    stutterPermutations,
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
    elif sum(n % 2 for n in sig) >= 1:
        return 1
    else:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )


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
    if sum(n % 2 for n in sig) == 1 or sum(n % 2 for n in sig) >= 3:
        # All-but-one-even signature
        for i, t in enumerate(transformer[:-1]):
            end_tuple_order.append((transformer[i + 1], t))
        # end_tuple_order.append((transformer[0], transformer[-1]))
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
        # end_tuple_order.append((0, len(sorted_sig) - 1, 0))
        transformed_end_tuple_order = transform(end_tuple_order, transformer)
        return transformed_end_tuple_order
    elif sum(n % 2 for n in sig) == 2:
        # now place one of the odd indices at the end and subtract 1 for every index after the odd indices
        ordered_tails = [(i,) for i, s in enumerate(sig) if s % 2 == 0]
        ordered_tails.append((next(i for i, s in enumerate(sig) if s % 2 == 1),))
        for i in range(len(ordered_tails) - 1):
            end_tuple_order.append(
                (ordered_tails[(i + 1) % len(ordered_tails)] + ordered_tails[i])
            )
        return end_tuple_order
    else:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )


def find_end_tuple_order(
    cycle_cover: list[list[tuple[int]]], force_three: bool = False
) -> list[tuple[int, ...]]:
    """
    Find the connecting end tuples in the order of the cycle cover.
    The end tuples are the tails of the cycles that are the nodes that connect them.
    The length of the end tuples is at most 3 but they can vary between end tuples.

    Args:
        cycle_cover (list[list[tuple[int]]]): The cycle cover to find the end tuples for.
        force_three (bool): If the end tuples should be of length 3.

    Returns:
        list[tuple[int, ...]]: The order of the end tuples of the cycles in the cycle cover.

    Raises:
        ValueError: If the cycle cover does not have connecting tails of length at most 3.
        ValueError: If the cycle cover depth is more than 1.
    """
    try:
        if not isinstance(cycle_cover[0][0][0], tuple):
            raise ValueError(
                f"Cycle cover should be a list of lists of tuples, got: {cycle_cover}"
            )
    except IndexError:
        raise ValueError(
            f"Cycle cover should contain at least one cycle, got: {cycle_cover}"
        )
    connecting_tails = []
    for i, cycle1 in enumerate(cycle_cover):
        cycle2 = cycle_cover[(i + 1) % len(cycle_cover)]
        tails1_3 = list(set([tuple(t[-3:]) for t in cycle1[0]]))
        tails2_3 = list(set([tuple(t[-3:]) for t in cycle2[0]]))
        # get the last 2 elements instead of 3 in a seperate variable
        tails1_2 = list(set([tuple(t[-2:]) for t in tails1_3]))
        tails2_2 = list(set([tuple(t[-2:]) for t in tails2_3]))
        # find the adjacent tails
        adjacent_tails = []
        if not force_three:
            for tail1 in tails1_2:
                for tail2 in tails2_2:
                    if adjacent(tail1, tail2):
                        adjacent_tails.append(tail1)
        if len(adjacent_tails) == 0:
            # try for length 3
            for tail1 in tails1_3:
                for tail2 in tails2_3:
                    if adjacent(tail1, tail2):
                        adjacent_tails.append(tail1)
        if len(adjacent_tails) == 0:
            print(f"tails1_3: {tails1_3}; tails2_3: {tails2_3}")
            print(f"signature of cycle1: {get_perm_signature(cycle1[0][0])}")
            raise ValueError(
                f"Could not find adjacent tails for cycle {i} and {i + 1} in cycle cover."
            )
        if len(adjacent_tails) > 1:
            # sort the tuples
            adjacent_tails = sorted(adjacent_tails)
        connecting_tails.append(adjacent_tails[0])
    return connecting_tails


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
    try:
        assert end in cut_cycle
    except AssertionError:
        raise AssertionError(
            f"Cycle from {cut_cycle[0]}-{cut_cycle[1]} to {cut_cycle[-1]} does not contain end node {end}."
        )
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
    cycle_cover: list[tuple[int, ...]],
    end_tuple_order: list[tuple[int, ...]],
) -> dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
    """
    Find parallel edges in the cycle cover. These edges are pairs of nodes in the cycle cover that have a tail that connects them to the next cycle.
    The tail is defined by the number of odd colors in the signature.

    Args:
        sig (tuple[int]): The signature of the permutation.
        cycle_cover (list[tuple[int, ...]]): The cycle cover to find parallel edges in.
        end_tuple_order (list[tuple[int, ...]]): The order of the end tuples of the cycles in the cycle cover.

    Returns:
        dict[list[tuple[tuple[int, ...], tuple[int, ...]]]]:
            A dictionary where the key is the pair of tails of the cycle that are combined and the value is the list of parallel edges.
            Each parallel edge is a tuple of two tuples of permutations (a permutation is a tuple of integers).
    """
    if len(cycle_cover) == 0:
        return []
    # generate the start tuples by swapping the first two elements of the tails
    start_tails = [swapPair(tail, 0) for tail in end_tuple_order]
    if len(cycle_cover) == 1:
        return {
            (end_tuple_order[0]): [
                filter_adjacent_edges_by_tail(cycle_cover[0], end_tuple_order[0])
            ],
            (start_tails[0]): [
                filter_adjacent_edges_by_tail(cycle_cover[0], start_tails[0])
            ],
        }
    assert len(cycle_cover) == len(end_tuple_order) + 1
    parallel_edges = {}
    for i, cycle in enumerate(cycle_cover[:-1]):
        parallel_edges[end_tuple_order[i]] = filter_adjacent_edges_by_tail(
            cycle[0], end_tuple_order[i]
        )
        parallel_edges[start_tails[i]] = filter_adjacent_edges_by_tail(
            cycle_cover[i + 1][0],
            start_tails[i],
        )
        if len(parallel_edges[end_tuple_order[i]]) == 0:
            print(f"end_tuple_order[{i}]: {end_tuple_order[i]}")
            print(f"cycle: {cycle}")
            print(
                f"parallel_edges[{end_tuple_order[i]}]: {parallel_edges[end_tuple_order[i]]}"
            )
            raise ValueError(f"Found no parallel edges for {end_tuple_order[i]}")
        if len(parallel_edges[start_tails[i]]) == 0:
            print(f"cover: {cycle_cover}")
            print(f"start_tails[{i}]: {start_tails[i]}")
            print(f"cycle_cover[{i + 1}]: {cycle_cover[i + 1]}")
            print(f"parallel_edges[{start_tails[i]}]: {parallel_edges[start_tails[i]]}")
            raise ValueError(f"Found no parallel edges for {start_tails[i]}")
    return parallel_edges


def get_transformer_tail_to_eto(end_tuple_start, tail, sig):
    transformer = [i for i in range(len(sig))]
    transformer[tail[0]] = end_tuple_start[0]
    transformer[tail[1]] = end_tuple_start[1]
    if end_tuple_start[0] not in tail:
        transformer[end_tuple_start[0]] = tail[0]
        if tail[0] == end_tuple_start[1]:
            transformer[end_tuple_start[0]] = tail[1]
    if end_tuple_start[1] not in tail:
        transformer[end_tuple_start[1]] = tail[1]
        if tail[1] == end_tuple_start[0]:
            transformer[end_tuple_start[1]] = tail[0]
    return transformer


def find_cross_edges(
    cycle_cover: list[list[tuple[int, ...]]],
    end_tuple_order: list[tuple[int, ...]],
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
        sig (tuple[int, ...]):
            The signature of the permutation.
        cycle_cover (list[list[tuple[int, ...]]]):
            The cycle cover to find cross edges in.
        end_tuple_order (list[tuple[int, ...]]):
            The order of the end tuples of the cycles in the cycle cover.

    Returns:
        dict[tuple[int, ...], list[tuple[tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], tuple[int, ...]]]]]:
            A dictionary where the key is a pair of tails of the cycle that are combined and the value is the list of cross edges.
            Each cross edge is a tuple of two tuples of permutations (a permutation is a tuple of integers).

    Raises:
        ValueError: If the cycle cover is empty.
    """
    if len(cycle_cover) == 0:
        raise ValueError("Cycle cover should contain at least one cycle.")
    parallel_edges = find_parallel_edges_in_cycle_cover(cycle_cover, end_tuple_order)
    if len(parallel_edges) < 2:
        raise ValueError(
            f"Cross edges should be found in at least two cycles; found {len(parallel_edges)}."
        )
    cross_edges = {}
    print(
        f"Looking for cross edges in signature {get_perm_signature(get_first_element(cycle_cover))}"
    )
    for tail1, parallel_edges1 in parallel_edges.items():
        tail2 = swapPair(tail1, 0)
        if (tail1, tail2) in cross_edges or (tail2, tail1) in cross_edges:
            continue
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
            write_cross_edge_ratio_to_file(cross_edges, tail1, tail2)
    for tail1, tail2 in cross_edges.keys():
        print(f"cross edges {(tail1, tail2)}: {sorted(cross_edges[(tail1, tail2)])}")
        # if get_perm_signature(get_first_element(cycle_cover)) == (5, 3, 3):
        #     quit()
    return cross_edges


def write_cross_edge_ratio_to_file(
    cross_edges: dict[
        tuple[int, ...],
        list[
            tuple[
                tuple[tuple[int, ...], tuple[int, ...]],
                tuple[tuple[int, ...], tuple[int, ...]],
            ],
        ],
    ],
    tail1: tuple[int, ...],
    tail2: tuple[int, ...],
    prompt_keep_old_csv: bool = False,
) -> None:
    """
    Writes the cross edge ratio to a csv file; `./crossedges.csv`. If the file doesn't exist, it creates it.

    Args:
        cross_edges (dict[tuple[int, ...], list[tuple[tuple[int, ...], tuple[int, ...]]]]): The cross edges to write to the file.
        tail1 (tuple[int, ...]): The first tail of the cross edge.
        tail2 (tuple[int, ...]): The second tail of the cross edge.

    Returns:
        None

    Raises:
        ValueError: If the cross edge is not found in the cross edges dictionary.
    """
    subsig_from = get_perm_signature(
        cross_edges[(tail1, tail2)][0][0][0][: -len(tail1) + 1]
    )
    total_edges_from = multinomial(subsig_from) - len(stutterPermutations(subsig_from))
    cross_edges_count = len(cross_edges[(tail1, tail2)])
    fraction_ratio = f"{Fraction(len(cross_edges[(tail1, tail2)]), total_edges_from).numerator}/{Fraction(len(cross_edges[(tail1, tail2)]), total_edges_from).denominator}"
    print(
        f"Cross edge {(tail1, tail2)} has a ratio of {cross_edges_count}/{total_edges_from} = {fraction_ratio}"
    )

    assert len(cross_edges[(tail1, tail2)]) > 0
    result_name = "./result.csv"
    original_name = "./crossedges.csv"
    # creat the file if it doesn't exist
    if not os.path.exists(original_name):
        with open(original_name, "w", newline=""):
            pass
    keep_old = False
    with open(original_name, "r", newline="") as source, open(
        result_name, "w", newline=""
    ) as result:
        reader = csv.reader(source, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
        writer = csv.writer(
            result, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONE
        )

        # if the file is empty, make the header
        if sum(1 for _ in reader) == 0:
            header = [
                "signature_length",
                "signature",
                "subsig_to",
                "subsig_from",
                "tail_to",
                "tail_from",
                "cross_edges_count",
                "multinomial_to",
                "multinomial_from",
                "ratio",
                "cross_edge",
            ]
            read_list = []
            # get the header
        else:
            source.seek(0)
            header = next(reader, None)
            read_list = [
                [
                    int(line[0]),
                    literal_eval(line[1]),
                    literal_eval(line[2]),
                    literal_eval(line[3]),
                    literal_eval(line[4]),
                    literal_eval(line[5]),
                    int(line[6]),
                    int(line[7]),
                    int(line[8]),
                    line[9],
                    literal_eval(line[10]),
                ]
                for line in reader
            ]
        writer.writerow(header)

        sig = get_perm_signature(cross_edges[(tail1, tail2)][0][0][0])
        subsig_to = get_perm_signature(
            cross_edges[(tail1, tail2)][0][1][0][: -len(tail1) + 1]
        )
        tail_to = cross_edges[(tail1, tail2)][0][1][0][-len(tail1) + 1 :]
        total_edges_to = multinomial(subsig_to) - len(stutterPermutations(subsig_to))
        tail_from = cross_edges[(tail1, tail2)][0][0][0][-len(tail1) + 1 :]
        chosen_edge = min(cross_edges.get((tail1, tail2)))[0]
        new_line = [
            len(sig),
            sig,
            subsig_to,
            subsig_from,
            tail_to,
            tail_from,
            cross_edges_count,
            total_edges_to,
            total_edges_from,
            fraction_ratio,
            chosen_edge,
        ]
        index = bisect.bisect_left(
            read_list, new_line, key=lambda x: [x[0], x[1], x[2], x[3]]
        )
        # check if the new line is already in the file
        if index == reader.line_num == 0:
            writer.writerow(new_line)
        else:
            old_line = read_list[index - 1]
            if (
                old_line[0] == len(sig)
                and old_line[1] == sig
                and old_line[2] == subsig_to
                and old_line[3] == subsig_from
                and not old_line[6] == cross_edges_count
            ):
                print(
                    f"\033[1m\033[91mCross edge {(tail1, tail2)} already in cross edges file;\n old line: {old_line};\n new line: {new_line} \033[0m\033[0m"
                )
                if prompt_keep_old_csv:
                    keep_old_value = input("Do you want to keep the old line? (y/n)")
                    if keep_old_value.lower() == "no" or keep_old_value.lower() == "n":
                        read_list.insert(index, new_line)
                        writer.writerows(read_list)
                    else:
                        keep_old = True
                else:
                    read_list.insert(index, new_line)
                    writer.writerows(read_list)
            elif (
                old_line[0] == len(sig)
                and old_line[1] == sig
                and old_line[2] == subsig_to
                and old_line[3] == subsig_from
                and old_line[6] == cross_edges_count
            ):
                keep_old = True
            else:
                read_list.insert(index, new_line)
                writer.writerows(read_list)
    if not keep_old:
        os.remove(original_name)
        os.rename(result_name, original_name)


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
    if cross_edges.get((tail, next_tail)) is None:
        raise ValueError(
            f"Cross edge {(tail, next_tail)} not found in cross edges from signature {get_perm_signature(cycle_to_cut[0])}. Cross edges keys: {cross_edges.keys()}."
        )
    # take the lexicographically smallest cross edge
    cross_edge = min(cross_edges.get((tail, next_tail)))[0]
    if cross_edge is None:
        raise ValueError(
            f"Cross edge {(tail, next_tail)} not found in cross edges {cross_edges}."
        )
    print(
        f"cycle_to_cut tails unique tails: {list(set([tuple(t[-2:]) for t in cycle_to_cut]))}"
    )
    ce0_idx = cycle_to_cut.index(cross_edge[0])
    ce1_idx = cycle_to_cut.index(cross_edge[1])
    try:
        assert abs(ce0_idx - ce1_idx) == 1
    except AssertionError:
        raise AssertionError(
            f"Cross edge {cross_edge} in {get_perm_signature(get_first_element(cycle_to_cut))} is not adjacent in the cycle:\n{cycle_to_cut[ce0_idx-1:ce0_idx+2]} and {cycle_to_cut[ce1_idx-1:ce1_idx+2]}."
        )
    if ce0_idx < ce1_idx:
        splitPathIn2(cycle_to_cut, cross_edge[0])
        return splitPathIn2(cycle_to_cut, cross_edge[0])
    else:
        return splitPathIn2(cycle_to_cut, cross_edge[1])


def connect_single_cycle_cover(
    single_cycle_cover: list[tuple[int, ...]],
    end_tuple_order: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """
    Connect a single list of cycles to form a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.

    Args:
        sig (tuple[int, ...]): The signature of the permutations. Must have at least one element.
        single_cycle_cover (list[tuple[int, ...]]): The single cycle cover to connect.
        end_tuple_order (list[tuple[int, ...]]): The order of the last elements of the cycles.

    Returns:
        list[tuple[int, ...]]:
            The connected cycle cover as a list of tuples, where each tuple represents a permutation.\n
            The last element of the last tuple is the first element of the first tuple.
    """
    # The cycles are split on the last elements
    tail_length = len(end_tuple_order[0])
    cross_edges = {}
    # cross_edges = find_cross_edges(single_cycle_cover, end_tuple_order)
    sig = get_perm_signature(get_first_element(single_cycle_cover))
    if sum(n % 2 for n in sig) == 1:
        print(f"Signature {sig} has one odd number.")
        for tail in end_tuple_order:
            tail_sig = list(get_perm_signature(tail)) + [0] * (
                len(list(sig)) - len(get_perm_signature(tail))
            )
            newsig = [n - tail_sig[i] for i, n in enumerate(sig)]
            # the cut node is the
            cut_node_sig = sorted(
                [(i, n - tail_sig[i]) for i, n in enumerate(sig)],
                key=lambda x: [x[1] % 2 == 0, -x[1]],
            )
            print(f"cutnodesig: {cut_node_sig}")
            node1 = tuple(
                [
                    cut_node_sig[i][0]
                    for i in range(len(cut_node_sig))
                    for _ in range(cut_node_sig[i][1])
                ]
            )
            print(f"node1 before tail: {node1}")
            node2 = node1 + swapPair(tail, 0)
            node1 = node1 + tail
            print(f"newsig: {newsig} and tail {tail}")
            print(f"node1: {node1} node2: {node2}")
            swapidx = -(
                tail_length
                + [
                    cut_node_occ[1]
                    for cut_node_occ in cut_node_sig
                    if cut_node_occ[1] > 0
                ][-1]
                + 1
            )
            cross_edges[(tail, swapPair(tail, 0))] = [
                (
                    (node1, swapPair(node1, swapidx)),
                    (node2, swapPair(node2, swapidx)),
                )
            ]
        print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    elif sum(n % 2 for n in sig) == 2:
        print(f"Signature {sig} has two odd numbers.")
        for i, c in enumerate(single_cycle_cover):
            print(
                f"unique tails in cycle {i}: {list(set([tuple(t[-3:]) for t in c[0]]))}"
            )
        print(f"end tuples in cycle cover:")
        for tail in end_tuple_order:
            tail_sig = list(get_perm_signature(tail)) + [0] * (
                len(list(sig)) - len(get_perm_signature(tail))
            )
            newsig = [n - tail_sig[i] for i, n in enumerate(sig)]
            # first all even indices (reversed); then the odd indices; then the rest
            even_tuples = [(i,) * el for i, el in enumerate(newsig) if el % 2 == 0]
            node1 = tuple()
            for el in even_tuples:
                node1 += el
            odd_tuples = sorted(
                [(i,) * el for i, el in enumerate(newsig) if el % 2 == 1], reverse=True
            )
            for el in odd_tuples:
                node1 += el
            node2 = node1 + swapPair(tail, 0)
            node1 = node1 + tail
            print(f"newsig: {newsig} and tail {tail}")
            print(f"node1: {node1} node2: {node2}")
            cross_edges[(tail, swapPair(tail, 0))] = [
                (
                    (node1, swapPair(node1, sum(len(i) for i in even_tuples) - 1)),
                    (node2, swapPair(node2, sum(len(i) for i in even_tuples) - 1)),
                )
            ]
        print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    elif sum(n % 2 for n in sig) >= 3:
        print(f"Signature {sig} has three or more odd numbers.")
        for tail in end_tuple_order:
            tail_sig = list(get_perm_signature(tail)) + [0] * (
                len(list(sig)) - len(get_perm_signature(tail))
            )
            # newsig is sorted
            unsorted_newsig = [(i, n - tail_sig[i]) for i, n in enumerate(sig)]
            newsig = sorted(
                unsorted_newsig, key=lambda x: [x[1] % 2 == 1, -x[1]], reverse=True
            )
            odd_elements = [(i, n) for i, n in newsig if n % 2 == 1 and n > 0]
            even_elements = [(i, n) for i, n in newsig if n % 2 == 0 and n > 0]
            node1 = (odd_elements[0][0],) * odd_elements[0][1]
            for i, el in even_elements:
                node1 += (i,) * el
            for i, n in odd_elements[1:]:
                node1 += (i,) * n
            if len(even_elements) > 1:
                swapidx = odd_elements[0][1] + even_elements[0][1] - 1
            else:
                swapidx = odd_elements[0][1] - 1
            node2 = node1 + swapPair(tail, 0)
            node1 = node1 + tail
            print(
                f"newsig: {newsig} from {[n for n in newsig if n != 0]} and tail {tail} swapidx {newsig[0][1]+newsig[1][1]-1}"
            )
            print(f"node1: {node1} node2: {node2}")
            cross_edges[(tail, swapPair(tail, 0))] = [
                (
                    (node1, swapPair(node1, swapidx)),
                    (node2, swapPair(node2, swapidx)),
                )
            ]
        print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    elif all(n % 2 == 0 for n in sig):
        print(f"Signature {sig} has all even numbers.")
        for tail in end_tuple_order:
            tail_sig = list(get_perm_signature(tail)) + [0] * (
                len(list(sig)) - len(get_perm_signature(tail))
            )
            newsig = [n - tail_sig[i] for i, n in enumerate(sig)]
            odd_el = [(i, n) for i, n in enumerate(newsig) if n % 2 == 1]
            # odd_el^{k_{odd_el}}} 0^{k_0} 1^{k_1} 2^{k_2} ... tail - odd_el^{k_{odd_el}} 0 odd_el 0^{k_0-1} 1^{k_1} 2^{k_2-1} ... tail
            # odd_el^{k_{odd_el}}} 0^{k_0} 1^{k_1} 2^{k_2} ... swapTail - odd_el^{k_{odd_el}} 0 odd_el 0^{k_0-1} 1^{k_1} 2^{k_2-1} ... swapTail
            node1 = (odd_el[0][0],) * odd_el[0][1]
            even_elements = [(i, n) for i, n in enumerate(newsig) if n % 2 == 0]
            for i, el in even_elements:
                node1 += (i,) * el
            for i, n in odd_el[1:]:
                node1 += (i,) * n
            if len(odd_el) > 1:
                swapidx = (
                    odd_el[0][1] + sum(even_el[1] for even_el in even_elements) - 1
                )
            else:
                swapidx = odd_el[0][1] - 1
            node2 = node1 + swapPair(tail, 0)
            node1 = node1 + tail
            print(f"newsig: {newsig} el {odd_el} tail {tail}")
            print(f"node1: {node1} node2: {node2}")
            cross_edges[(tail, swapPair(tail, 0))] = [
                (
                    (node1, swapPair(node1, swapidx)),
                    (node2, swapPair(node2, swapidx)),
                )
            ]
        print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    else:
        raise ValueError(f"Signature {sig} has an unexpected number of odd numbers.")
    start_cycles, end_cycles = split_sub_cycle_for_next_cross_edge(
        single_cycle_cover[0][0], end_tuple_order[0], cross_edges
    )
    print(
        f"used cross edges: {cross_edges[(end_tuple_order[0], swapPair(end_tuple_order[0], 0))]}"
    )
    # start_cycles, end_cycles = split_sub_cycle_for_next(single_list, tail)
    for i, cycle_list in enumerate(single_cycle_cover[1:], start=1):
        print(f"cut nodes start: {start_cycles[-1]} end: {end_cycles[0]}")
        cut_cycle = cut_sub_cycle_to_past(
            cycle_list[0],
            swapPair(start_cycles[-1], -tail_length),
            swapPair(end_cycles[0], -tail_length),
        )
        if i < len(single_cycle_cover) - 1:
            new_tail = end_tuple_order[i]
            # cycle_split = split_sub_cycle_for_next(cut_cycle, new_tail)
            cycle_split = split_sub_cycle_for_next_cross_edge(
                cut_cycle,
                new_tail,
                cross_edges,
            )
            start_cycles += cycle_split[0]
            end_cycles = cycle_split[1] + end_cycles
        else:
            start_cycles += cut_cycle
    return start_cycles + end_cycles
