import bisect
import csv
import os
from ast import literal_eval
from fractions import Fraction

from tqdm import tqdm

from helper_operations.path_operations import adjacent, get_first_element
from helper_operations.permutation_graphs import (
    get_perm_signature,
    multinomial,
    stutterPermutations,
    swapPair,
)


def find_end_tuple_order(
    cycle_cover: list[list[tuple[int, ...]]], force_three: bool = False
) -> list[tuple[int, ...]]:
    """
    Find the connecting end tuples in the order of the cycle cover.
    The end tuples are the tails of the cycles that are the nodes that connect them.
    The length of the end tuples is at most 3 but they can vary between end tuples.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to find the end tuples for.
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
        print(
            f"cross edges {(tail1, tail2)}: {sorted(cross_edges[(tail1, tail2)])} (len: {len(cross_edges[(tail1, tail2)])})"
        )
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
