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
    tail_len: int,
    sig: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """
    Merges the cycles in the cycle cover for all-even and all-but-one-even permutations.
    The cycles are connected to form a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.
    The end tuples of the cycles are based on the last `tail_length` elements of the cycle, which is 2 for all-even and 1 for all-but-one-even permutations.
    The cycles are split on the last elements and connected to the next cycle.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to merge.
        tail_length (int): The length of the suffix of the cycle that is used to connect the cycles.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list[tuple[int, ...]]: The merged cycle cover
    """
    # while the depth of the list is more than 2, we need to connect the previous cycles
    single_cycle_cover = connect_recursive_cycles(cycle_cover_segments, tail_len, sig)
    # The cycles are split on the last elements
    end_tuple_order = generate_end_tuple_order(single_cycle_cover, tail_len)
    # The first cycle is a cycle
    # Ensure that the first cycle has start and end nodes that have the suffix _100
    tail = end_tuple_order[0]
    single_list = get_single_list(single_cycle_cover)
    start_cycles, end_cycles = split_sub_cycle_for_next(single_list, tail)
    print(f"cut nodes 0: {start_cycles[-1]}, {end_cycles[0]}")
    for i, cycle_list in enumerate(single_cycle_cover[1:-1], start=1):
        cut_cycle = cut_sub_cycle_to_past(
            cycle_list[0],
            swapPair(start_cycles[-1], -(tail_len + 1)),
            swapPair(end_cycles[0], -(tail_len + 1)),
        )
        new_tail = end_tuple_order[i]
        cycle_split = split_sub_cycle_for_next(cut_cycle, new_tail)
        start_cycles += cycle_split[0]
        end_cycles = cycle_split[1] + end_cycles
        print(f"cut nodes {i}: {start_cycles[-1]}, {end_cycles[0]}")

    # The last cycle is a cycle and has to be pasted to the past one but not cut in itself
    cut_cycle = cut_sub_cycle_to_past(
        single_cycle_cover[-1][0],
        swapPair(start_cycles[-1], -(tail_len + 1)),
        swapPair(end_cycles[0], -(tail_len + 1)),
    )
    start_cycles += cut_cycle
    print(f"cut nodes {len(single_cycle_cover)-1}: {start_cycles[-1]}")
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
        tail_length = 1
        return merge_even_signatures(cycle_cover, tail_length, sig)
    elif all(n % 2 == 0 for n in sig):
        # The cycles are split on the last two elements
        tail_length = 2
        return merge_even_signatures(cycle_cover, tail_length, sig)
    else:
        print(f"Not sure why this would happen, but happened for {sig}")


def connect_recursive_cycles(
    cycle_cover: list[list[tuple[int, ...]]], tail_length: int, sig: tuple[int, ...]
) -> list[list[tuple[int, ...]]]:
    """
    Annotates the connect_previous_cycles function with types.

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to connect.
        tail_length (int): The length of the suffix of the cycle that is used to connect the cycles.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list[list[tuple[int, ...]]]: The connected cycle cover.
    """
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
            print(
                f"subsig: {subsig}, last element: {last_element}, previous signature: {sig}"
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
    cycle_cover: list[list[tuple[int, ...]]], tail_length: int
) -> list[tuple[int, ...]]:
    """
    Generates the order of the end tuples of the cycles in the cycle cover.
    The end tuples are the last `tail_length` elements of the cycle.
    They are formed in two orders:\n
    - **All-even**: _00, _01/_10, _11, _12/_21, _22, _02/_20, _23/_32, _33, _03/_30, _31/_13, _34/_43, _44, _04/_40, _41/_14, _42/_24
    - **All-but-one-even**: _0, _1, _2, _3, _4, _5,

    Args:
        cycle_cover (list[list[tuple[int, ...]]]): The cycle cover to generate the end tuple order for.
        tail_length (int): The length of the end tuple.

    Returns:
        list[tuple[int, ...]]: The order of the end tuples of the cycles in the cycle

    Raises:
        ValueError: If there is more than one change in consecutive end tuples.
    """
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
        AssertionError: If the start and end nodes are not adjacent in the cycle.
    """
    cut_cycle = cutCycle(cycle_to_cut, start)
    if cut_cycle[-1] == end:
        return cut_cycle
    if cut_cycle[1] == end:
        return cut_cycle[:1] + cut_cycle[1:][::-1]
    else:
        raise AssertionError(
            f"Start and end nodes {start} and {end} are not found in the cycle {cut_cycle}. "
            f"Start node at index {cut_cycle.index(start)} and end node at index {cut_cycle.index(end)}."
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
