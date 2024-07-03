import argparse
import collections

from cycle_cover import generate_cycle_cover
from helper_operations.path_operations import (
    adjacent,
    cutCycle,
    cycleQ,
    get_first_element,
    get_single_list,
    pathQ,
    shorten_cycle_cover,
    splitPathIn2,
)
from helper_operations.permutation_graphs import (
    extend,
    extend_cycle_cover,
    selectByTail,
    swapPair,
)
from visualization import is_stutter_permutation


def connect_subcycle_cover(subcyles: list[list], sig: tuple[int, ...]) -> list:
    """
    If the cycle cover is a subcycle cover, connect the subcycles to a Hamiltonian cycle on the non-stutter permutations of a neighbor-swap graph.
    Checks whether the subcycle cover is a list of lists, and takes the first list (not a tuple) of length > 1, then connects the subcycles to a Hamiltonian cycle.

    Args:
        subcyles (list[list]): The subcycle cover to connect.
        sig (tuple[int, ...]): The permutation signature, number of occurrences of each element.

    Returns:
        list: The connected subcycle cover.
    """
    if not all(isinstance(subcycle, list) for subcycle in subcyles):
        raise ValueError("Subcycle cover is not a list of lists.")
    subcycle = next((subcycle for subcycle in subcyles if len(subcycle) > 1), None)
    if subcycle is None:
        raise ValueError("No subcycle found in subcycle cover.")
    return connect_cycle_cover([subcycle], sig)


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
    # If there is one color that occurs an odd number of times
    elif isinstance(cycle_cover[0][0], int):
        return cycle_cover
    elif any(n % 2 == 1 for n in sig):
        # Loop over the cycles in the cover and connect the cycle at index `i` ends with an element of color `i`
        tail_length = 1
        single_cycle_cover = connect_previous_cycles(cycle_cover, tail_length, sig)
        # The cycles are split on the last elements
        print(f"Single cycle cover: {single_cycle_cover}")
        end_tuple_order = generate_end_tuple_order(single_cycle_cover, tail_length)
        # The first cycle is a cycle
        # Ensure that the first cycle has start and end nodes that have the suffix _100
        tail = end_tuple_order[0]
        start_cycles, end_cycles = cut_sub_cycle_for_next(
            single_cycle_cover[0][0], tail
        )
        for i, cycle_list in enumerate(single_cycle_cover[1:-1], start=1):
            cut_cycle = cut_sub_cycle_to_past(
                cycle_list[0],
                swapPair(start_cycles[-1], -(tail_length + 1)),
                swapPair(end_cycles[0], -(tail_length + 1)),
            )
            new_tail = end_tuple_order[i]
            cycle_split = cut_sub_cycle_for_next(cut_cycle, new_tail)
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
    elif all(n % 2 == 0 for n in sig):
        # The cycles are split on the last two elements
        tail_length = 2
        single_cycle_cover = connect_previous_cycles(cycle_cover, tail_length, sig)
        print(f"Single cycle cover: {single_cycle_cover}")
        end_tuple_order = generate_end_tuple_order(single_cycle_cover, tail_length)
        # The first cycle is a cycle
        # Ensure that the first cycle has start and end nodes that have the suffix _100
        tail = end_tuple_order[0]
        print(
            f"End tuple order: {end_tuple_order}, tail: {tail}, cycle cover: {single_cycle_cover[0][0]}"
        )
        single_list = get_single_list(single_cycle_cover)
        start_cycles, end_cycles = cut_sub_cycle_for_next(single_list, tail)
        for i, cycle_list in enumerate(single_cycle_cover[1:-1], start=1):
            print(f"index: {i}, signature: {sig}, last element: {start_cycles[-1]}")
            cut_cycle = cut_sub_cycle_to_past(
                cycle_list[0],
                swapPair(start_cycles[-1], -(tail_length + 1)),
                swapPair(end_cycles[0], -(tail_length + 1)),
            )
            new_tail = end_tuple_order[i]
            cycle_split = cut_sub_cycle_for_next(cut_cycle, new_tail)
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
    else:
        print(f"Not sure why this would happen, but happened for {sig}")


def connect_previous_cycles(
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
    for i, nested_cycle in enumerate(cycle_cover):
        if (
            isinstance(nested_cycle, list)
            and len(nested_cycle) > 1
            and isinstance(nested_cycle[0], list)
        ):
            # we need to remove the last element from every list in the nested cycle to connect them
            last_element = get_first_element(nested_cycle)[-(tail_length):]
            shortened_cycle = shorten_cycle_cover(
                [[nest] for nest in nested_cycle], last_element
            )
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
            # subsig = tuple([n - 1 if i == last_element[0] else n for i, n in enumerate(sig)])
            connected_shortened = connect_cycle_cover(shortened_cycle, subsig)
            # Now we need to add the last element back to the connected shortened cycle
            connected = extend_cycle_cover([connected_shortened], last_element)
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
        ValueError: If there is more than one change in the end tuple order.
    """
    end_tuple_order = []
    for c in cycle_cover:
        end_tuple_order.append(get_first_element(c)[-tail_length:])
        # Now prepend to every end_tuple the element that is different in the next end_tuple
    for i in range(len(end_tuple_order) - 1):
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
    print(f"End tuple order: {end_tuple_order}")
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


def cut_sub_cycle_for_next(
    cycle_to_cut: list[tuple[int, ...]], tail: tuple[int, ...]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """
    Cuts the subcycle cover at nodes that end with `tail` and opens them such that the next cycle can be connected to the current cycle.
    The tail nodes are the nodes that should be at the end of the cycle.
    The first two nodes of the tail are swapped to ensure they are not forming stutter permutations.

    Args:
        cycle_to_cut (list[tuple[int, ...]]): The cycle to cut open at nodes with the provided tail. Both the node before and after the cut should end with `tail`.
        tail (tuple[int, ...]): The tails that the nodes should end with.

    Returns:
        tuple[list[tuple[int, ...]], list[tuple[int, ...]]]: The cycle cover cut open between the two nodes with the provided tail.

    Raises:
        ValueError: If not enough tail nodes are found in the first cycle.
        ValueError: If no valid tail nodes are found.
    """
    tail_nodes = selectByTail(cycle_to_cut, tail)
    if len(tail_nodes) < 2:
        print(f"Cycle to cut: {cycle_to_cut}, tail: {tail}")
        raise ValueError(
            f"Not enough tail nodes found in the first cycle: {tail_nodes}. The tail was {tail}."
        )
    print(f"Tail nodes: {tail_nodes}")
    print(
        f"swapped   : {[swapPair(tail_node, -len(tail)) for tail_node in tail_nodes]}, tail: {tail}"
    )
    # Now check if swapping the first two elements of the tail nodes gives a stutter permutation\
    tail_idx = 0
    while (
        is_stutter_permutation(swapPair(tail_nodes[tail_idx], -len(tail)))
        or is_stutter_permutation(swapPair(tail_nodes[tail_idx + 1], -len(tail)))
        or not adjacent(tail_nodes[tail_idx], tail_nodes[tail_idx + 1])
    ):
        tail_idx += 1
        if tail_idx == len(tail_nodes) - 1:
            # manually check the last-first combination
            if (
                is_stutter_permutation(swapPair(tail_nodes[-1], -len(tail)))
                or is_stutter_permutation(swapPair(tail_nodes[0], -len(tail)))
                or not adjacent(tail_nodes[-1], tail_nodes[0])
            ):
                raise ValueError(f"No valid tail nodes found: {tail_nodes}")
            else:
                break
    return splitPathIn2(cycle_to_cut, tail_nodes[tail_idx])


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
    cycle_cover = generate_cycle_cover(sig)
    assert len(cycle_cover) > 0
    if len(cycle_cover) == 1:
        cycle = cycle_cover[0]
        if args.verbose:
            print(f"Cycle cover is a cycle: {cycle}")
        print(f"Cycle cover is a cycle {cycleQ(cycle)} and a path {pathQ(cycle)}")
    else:
        connected_cycle_cover = connect_cycle_cover(cycle_cover, sig)
        if args.verbose:
            print(f"Connected cycle cover: {connected_cycle_cover}")
        print(
            f"Cycle cover is a cycle {cycleQ(connected_cycle_cover)} and a path {pathQ(connected_cycle_cover)}"
        )
        # stutter_count = len(stutterPermutations(sig))
        # print(
        #     f"Cycle of length {len(connect_cycle_cover)}/{len(set(connect_cycle_cover))}/{multinomial(sig)} (contains {stutter_count} stutters) so in total {stutter_count + len(cycle_cover)} permutations."
        # )
