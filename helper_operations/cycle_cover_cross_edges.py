from helper_operations.permutation_graphs import get_perm_signature, swapPair


def get_all_even_cross_edges(
    end_tuple_order: list[tuple[int, ...]],
    cross_edges: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[tuple[tuple[int, ...], tuple[int, ...]]],
    ],
    sig: tuple[int, ...],
) -> dict[
    tuple[tuple[int, ...], tuple[int, ...]],
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    """
    Get all cross edges for a signature with all even occurring colors

    Args:
        end_tuple_order (list[tuple[int, ...]]): The order of the end tuples of the cycles in the cycle cover.
        cross_edges (dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]): The cross edges to add to.
        sig (tuple[int, ...]): The signature of the permutation.

    Returns:
        dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]: The cross edges with all even occurring colors
    """
    print(f"Signature {sig} has all even numbers.")
    for tail in end_tuple_order:
        tail_sig = list(get_perm_signature(tail)) + [0] * (
            len(list(sig)) - len(get_perm_signature(tail))
        )
        newsig = [n - tail_sig[i] for i, n in enumerate(sig)]
        odd_el = sorted(
            [(i, n) for i, n in enumerate(newsig) if n % 2 == 1],
            key=lambda x: [x[0] == tail[2], x[1], -x[0]],
            reverse=True,
        )
        node1 = tuple()
        for i, n in odd_el[:1]:
            node1 += (i,) * n
        even_elements = sorted(
            [(i, n) for i, n in enumerate(newsig) if n % 2 == 0],
            key=lambda x: [x[0] in tail[:2], x[1], -x[0]],
            reverse=True,
        )
        for i, el in even_elements:
            node1 += (i,) * el
        for i, n in odd_el[1:]:
            node1 += (i,) * n
        swapidx = odd_el[0][1] - 1
        node2 = node1 + swapPair(tail, 0)
        node1 = node1 + tail
        print(f"newsig: {newsig} el {odd_el} tail {tail}")
        print(f"node1: {node1} node2: {node2} with swap {swapidx}")
        cross_edges[(tail, swapPair(tail, 0))] = [
            (
                (node1, swapPair(node1, swapidx)),
                (node2, swapPair(node2, swapidx)),
            )
        ]
    print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    return cross_edges


def generate_one_odd_cross_edges(
    end_tuple_order: list[tuple[int, ...]],
    cross_edges: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[tuple[tuple[int, ...], tuple[int, ...]]],
    ],
    sig: tuple[int, ...],
) -> dict[
    tuple[tuple[int, ...], tuple[int, ...]],
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    """
    Get all cross edges for a signature with one odd and the rest even occurring colors

    Args:
        end_tuple_order (list[tuple[int, ...]]): The order of the end tuples of the cycles in the cycle cover.
        cross_edges (dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]): The cross edges to add to.
        sig (tuple[int, ...]): The signature of the permutation.

    Returns:
        dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]: The cross edges with one odd - rest even occurring colors
    """
    print(f"Signature {sig} has one odd number.")
    # find_cross_edges(single_cycle_cover, end_tuple_order)
    for tail in end_tuple_order:
        tail_sig = list(get_perm_signature(tail)) + [0] * (
            len(list(sig)) - len(get_perm_signature(tail))
        )
        [n - tail_sig[i] for i, n in enumerate(sig)]
        odd_elements = sorted(
            [
                (i, n - (i in tail))
                for i, n in enumerate(sig)
                if ((n - (i in tail)) % 2 == 1)
            ],
            key=lambda x: [x[0] not in tail, x[1]],
            reverse=True,
        )
        even_elements = sorted(
            [
                (i, n - (i in tail))
                for i, n in enumerate(sig)
                if ((n - (i in tail)) % 2 == 0)
            ],
            key=lambda x: [x[0] not in tail, x[1]],
            reverse=True,
        )

        node1 = tuple()
        for i, el in odd_elements[:1]:
            node1 += (i,) * el
        for i, el in even_elements:
            node1 += (i,) * el
        for i, el in odd_elements[1:]:
            node1 += (i,) * el
        node1 += tail
        node2 = swapPair(node1, -2)
        swapidx = odd_elements[0][1] - 1
        sig_min_tail = sorted(
            [n - (i == tail[1]) for i, n in enumerate(sig)],
            key=lambda x: [x % 2, x],
            reverse=True,
        )
        # the signatures odd-2-1 and even-odd-1 are exceptions here
        if (
            (sig_min_tail[0] % 2 == 1 and sig_min_tail[2] == 2) or sig_min_tail[1] == 1
        ) and len(sig) == 3:
            swapidx = odd_elements[0][1] + odd_elements[1][1] - 1
        cross_edges[(tail, swapPair(tail, 0))] = [
            (
                (node1, swapPair(node1, swapidx)),
                (node2, swapPair(node2, swapidx)),
            )
        ]
    print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    return cross_edges


def generate_two_odd_cross_edges(
    end_tuple_order: list[tuple[int, ...]],
    cross_edges: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[tuple[tuple[int, ...], tuple[int, ...]]],
    ],
    sig: tuple[int, ...],
) -> dict[
    tuple[tuple[int, ...], tuple[int, ...]],
    list[tuple[tuple[int, ...], tuple[int, ...]]],
]:
    """
    Get all cross edges for a signature with two odd and the rest even occurring colors

    Args:
        end_tuple_order (list[tuple[int, ...]]): The order of the end tuples of the cycles in the cycle cover.
        cross_edges (dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]): The cross edges to add to.
        sig (tuple[int, ...]): The signature of the permutation.

    Returns:
        dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[tuple[int, ...], tuple[int, ...]]]]: The cross edges with two odd - rest even occurring colors
    """
    print(f"Signature {sig} has one odd number.")
    for tail in end_tuple_order:
        three_odd_elements_sig = sorted(
            [(i, n - (i == tail[1])) for i, n in enumerate(sig)],
            key=lambda x: [x[1] % 2 == 0, x[0] == tail[1], x[0] != tail[0], x[1]],
            reverse=True,
        )
        node1 = tuple()
        for i, el in three_odd_elements_sig:
            node1 += (i,) * el
        # swapindex is the sum of all even elements and the first odd element - 1
        swapidx = (
            sum(even for _, even in three_odd_elements_sig if even % 2 == 0)
            + next(odd for _, odd in three_odd_elements_sig if odd % 2 == 1)
            - 1
        )
        node1 = node1 + (tail[1],)
        node2 = swapPair(node1, -2)
        cross_edges[(tail, swapPair(tail, 0))] = [
            (
                (node1, swapPair(node1, swapidx)),
                (node2, swapPair(node2, swapidx)),
            )
        ]
        print(
            f"three_odd_elements_sig: {three_odd_elements_sig}; node1: {node1} node2: {node2} swapidx: {swapidx}"
        )
    print(f"\033[1m\033[92mChosen cross edges:\n {cross_edges}\033[0m\033[0m")
    return cross_edges
