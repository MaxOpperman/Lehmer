from collections import Counter
from functools import cache

from helper_operations.cycle_cover_cross_edges import (
    generate_one_odd_cross_edges,
    generate_two_odd_cross_edges,
    get_all_even_cross_edges,
)
from helper_operations.path_operations import (
    find_last_distinct_adjacent_index,
    get_first_element,
    get_transformer,
    glue,
    transform,
)
from helper_operations.permutation_graphs import get_perm_signature, swapPair


def get_tail_length(sig: tuple[int, ...]) -> int:
    """
    Get the length of the tail to cut the cycle cover on.

    Args:
        sig (tuple[int, ...]): The signature of the permutation.

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
def generate_end_tuple_order(sig: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Generates the order of the end tuples of the cycles in the cycle cover.
    The end tuples are the tails of the cycles that are the nodes that connect them.
    They are cycles are ordered by their end tuples:\n
    - **All-even**: _00, _01/_10, _11, _12/_21, _22, , ...
    - **All-but-one-even**: _0, _1, _2, _3, _4, _5, ...

    Args:
        sig (tuple[int, ...]): The signature of the permutation.

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
            end_tuple_order.append((ordered_tails[-1] + ordered_tails[i]))
        return end_tuple_order
    else:
        raise ValueError(
            f"Signature should contain at most one odd number. Got {sig} with {sum(n % 2 for n in sig)} odd numbers."
        )


def get_two_odd_rest_even_cycle(
    single_cycle_cover: list[list[tuple[int, ...]]],
    end_tuple_order: list[tuple[int, ...]],
    cross_edges: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[tuple[tuple[int, ...], tuple[int, ...]]],
    ],
    sig: tuple[int, ...],
) -> list[tuple[int, ...]]:
    """
    Generate the Hamiltonian cycle for a signature with two odd and the rest even occurring colors
    Combines all the three odd signatures with a trailing even element to the first cycle with an odd trailing element.\
    
    Args:
        single_cycle_cover (list[list[tuple[int, ...]]]): The single cycle cover to connect.
        end_tuple_order (list[tuple[int, ...]]): The order of the last elements of the cycles.
        cross_edges (dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]): The cross edges to add to.
        sig (tuple[int, ...]): The signature of the permutation.
    
    Returns:
        list[tuple[int, ...]]: The connected cycle cover as a list of tuples, where each tuple represents a permutation.
    """
    generate_two_odd_cross_edges(end_tuple_order, cross_edges, sig)
    # the 2 odd case is different because we connect all individual cycles to the last one
    last_cycle = single_cycle_cover[-1][0]
    for i, cycle in enumerate(single_cycle_cover[:-1]):
        cross_edge = cross_edges[(end_tuple_order[i], swapPair(end_tuple_order[i], 0))][
            0
        ]
        print(f"cross_edge: {cross_edge}")
        last_cycle = glue(
            cycle[0],
            last_cycle,
            cross_edge[0],
            cross_edge[1],
        )
    return last_cycle


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
    cross_edges = {}
    # cross_edges = find_cross_edges(single_cycle_cover, end_tuple_order)
    sig = get_perm_signature(get_first_element(single_cycle_cover))
    if sum(n % 2 for n in sig) == 1:
        generate_one_odd_cross_edges(end_tuple_order, cross_edges, sig)
    elif sum(n % 2 for n in sig) == 2:
        return get_two_odd_rest_even_cycle(
            single_cycle_cover, end_tuple_order, cross_edges, sig
        )
    elif sum(n % 2 for n in sig) >= 3:
        print(
            f"Signature {sig} has three or more odd numbers. (total: {sum(n % 2 for n in sig)})"
        )
        # find_cross_edges(single_cycle_cover, end_tuple_order)
        for tail in end_tuple_order:
            newsig = [
                n - (i in tail) for i, n in enumerate(sig) if n - (i in tail) >= 0
            ]
            if sum(n % 2 for n in sig) % 2 == 1:
                even_elements = sorted(
                    [
                        (i, n if n % 2 == 0 else n - 1)
                        for i, n in enumerate(newsig)
                        if n >= 2
                    ],
                    key=lambda x: [-x[1], x[0]],
                    reverse=True,
                )
                # even_elements = [(i, n if n % 2 == 0 else n - 1) for i, n in enumerate(newsig) if n >= 2]
                odd_elements = sorted(
                    [(i, 1) for i, n in enumerate(newsig) if n % 2 == 1],
                    key=lambda x: [x[1]],
                    reverse=True,
                )
                swapidx = -1
                print(
                    f"newsig: {newsig} odd count in newsig {sum(n % 2 for n in newsig)} and evens; {sum(n % 2 == 0 for n in newsig)} even_elements: {even_elements} odd_elements: {odd_elements}"
                )
                node1 = tuple()
                for i, el in even_elements:
                    node1 += (i,) * el
                for i, el in odd_elements:
                    node1 += (i,) * el
                # if the signature has 3 odd numbers and the two items in the tail are not even
                if (
                    sum(n % 2 for n in sig) == 3
                    and swapidx == -1
                    and not any(sig[e] % 2 == 0 for e in tail)
                ):
                    if len(even_elements) > 1:
                        swapidx = sum(el for _, el in even_elements[:-1]) - 1
                    else:
                        swapidx = find_last_distinct_adjacent_index(node1)
                elif swapidx == -1:
                    swapidx = find_last_distinct_adjacent_index(node1)
                print(
                    f"node1: {node1} swapidx: {swapidx} (to get {swapPair(node1, swapidx)} with tails {tail, swapPair(tail, 0)}) those are elements {node1[swapidx]} and {node1[swapidx+1]} with occurences {newsig[node1[swapidx]]} and {newsig[node1[swapidx+1]]} and in the old sig {sig[node1[swapidx]]} and {sig[node1[swapidx+1]]}"
                )
                # check if the swap is between two elements that are adjacent in the neighbor-swap graph of length n-1

                node2 = node1 + swapPair(tail, 0)
                node1 = node1 + tail
                # check the number of even and odds in node1 and node2
            else:
                even_elements = sorted(
                    [(i, n) for i, n in enumerate(newsig) if n % 2 == 0],
                    key=lambda x: [x[1], x[0]],
                    reverse=True,
                )
                # even_elements = [(i, n if n % 2 == 0 else n - 1) for i, n in enumerate(newsig) if n >= 2]
                odd_elements = sorted(
                    [(i, n) for i, n in enumerate(newsig) if n % 2 == 1],
                    key=lambda x: [x[1]],
                    reverse=True,
                )
                node1 = (odd_elements[0][0],) * odd_elements[0][1]
                swapidx = len(node1) - 1
                for i, el in even_elements:
                    node1 += (i,) * el
                for i, el in odd_elements[1:]:
                    node1 += (i,) * el
                if sum(n % 2 for n in sig) > 4 or any(sig[e] % 2 == 0 for e in tail):
                    swapidx = find_last_distinct_adjacent_index(node1)
                elif (
                    sig[0] % 2 == 1
                    and sig[1] % 2 == 1
                    and sig[2:] == (1, 1)
                    and tail == (2, 1)
                ):
                    swapidx = find_last_distinct_adjacent_index(node1)
                print(f"newsig: {newsig} node1 {node1}, node2 swapidx {swapidx}")
                node2 = node1 + swapPair(tail, 0)
                node1 = node1 + tail
            print(
                f"newsig: {newsig} node1 {sum(c % 2 == 0 for c in Counter(node1[:-1]).values()), sum(c % 2 != 0 for c in Counter(node1[:-1]).values())}, node2 {sum(c % 2 == 0 for c in Counter(node2[:-1]).values()), sum(c % 2 != 0 for c in Counter(node2[:-1]).values())}"
            )
            cross_edges[(tail, swapPair(tail, 0))] = [
                (
                    (node1, swapPair(node1, swapidx)),
                    (node2, swapPair(node2, swapidx)),
                )
            ]
        print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    elif all(n % 2 == 0 for n in sig):
        get_all_even_cross_edges(end_tuple_order, cross_edges, sig)
    else:
        raise ValueError(f"Signature {sig} has an unexpected number of odd numbers.")
    result_cycle = single_cycle_cover[0][0]
    for i, tail in enumerate(end_tuple_order):
        next_tail = swapPair(tail, 0)
        if cross_edges.get((tail, next_tail)) is None:
            raise ValueError(
                f"Cross edge {(tail, next_tail)} not found in cross edges from signature {sig}. Cross edges keys: {cross_edges.keys()}."
            )
        cross_edge = cross_edges.get((tail, next_tail))[0]
        result_cycle = glue(
            result_cycle,
            single_cycle_cover[i + 1][0],
            cross_edge[0],
            cross_edge[1],
        )
    return result_cycle
