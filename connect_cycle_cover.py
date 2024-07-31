import argparse

from cycle_cover import generate_cycle_cover
from helper_operations.cycle_cover_connections import (
    cut_sub_cycle_to_past,
    find_cross_edges,
    generate_end_tuple_order,
    get_tail_length,
    split_sub_cycle_for_next_cross_edge,
)
from helper_operations.path_operations import (
    adjacent,
    cycleQ,
    get_first_element,
    get_transformer,
    pathQ,
    splitPathIn2,
    transform,
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
    tail_length = get_tail_length(sig)
    single_cycle_cover = []
    for nested_cycle in cycle_cover:
        if (
            isinstance(nested_cycle, list)
            and isinstance(nested_cycle[0], list)
            and isinstance(nested_cycle[0][0], list)
        ):
            # we need to remove the last element from every list in the nested cycle to connect them
            first_cycle_element = get_first_element(nested_cycle)

            # Get the new signature
            subsig = get_perm_signature(first_cycle_element[:-tail_length])
            sorted_subsig, subsig_transformer = get_transformer(subsig, lambda x: x[0])

            connected_shortened = get_connected_cycle_cover(sorted_subsig)
            # Now we need to add the last element back to the connected shortened cycle
            if isinstance(connected_shortened[0], tuple):
                connected_shortened = [connected_shortened]
            # now transform the connected shortened subsig back to the original values
            transformed_short = transform_cycle_cover(
                connected_shortened, subsig_transformer
            )
            connected = extend_cycle_cover(
                transformed_short, first_cycle_element[-tail_length:]
            )
            single_cycle_cover.append(connected)
        else:
            single_cycle_cover.append(nested_cycle)
    return single_cycle_cover


def _split_sub_cycle_for_next(
    cycle_to_cut: list[tuple[int, ...]], tail: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Unused\n
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
        if len(cover) == 1:
            return cover[0]
        elif isinstance(cover[0][0], int):
            return cover
        # If there is less than two odd occurring colors, we can connect the cycles using the recursive connection method
        # Loop over the cycles in the cover and connect the cycle at index `i` ends with an element of color `i`
        tail_length = get_tail_length(sig)
        # The cycles are split on the last elements
        end_tuple_order = generate_end_tuple_order(sig)
        # while the depth of the list is more than 2, we need to connect the previous cycles
        single_cycle_cover = connect_recursive_cycles(cover, sig)
        cross_edges = find_cross_edges(sig, single_cycle_cover)

        start_cycles, end_cycles = split_sub_cycle_for_next_cross_edge(
            single_cycle_cover[0][0], end_tuple_order[0], cross_edges
        )
        # start_cycles, end_cycles = split_sub_cycle_for_next(single_list, tail)
        for i, cycle_list in enumerate(single_cycle_cover[1:], start=1):
            cut_cycle = cut_sub_cycle_to_past(
                cycle_list[0],
                swapPair(start_cycles[-1], -(tail_length + 1)),
                swapPair(end_cycles[0], -(tail_length + 1)),
            )
            if i < len(single_cycle_cover) - 1:
                new_tail = end_tuple_order[i]
                # cycle_split = split_sub_cycle_for_next(cut_cycle, new_tail)
                cycle_split = split_sub_cycle_for_next_cross_edge(
                    cut_cycle, new_tail, cross_edges
                )
                start_cycles += cycle_split[0]
                end_cycles = cycle_split[1] + end_cycles
            else:
                start_cycles += cut_cycle
        return start_cycles + end_cycles


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
        f"with {len(connected_cycle_cover)}/{multinomial(sig)} (incl {stut_count} stutters is {stut_count+len(connected_cycle_cover)}) permutations from signature {get_perm_signature(connected_cycle_cover[-1])}."
    )
