from bisect import bisect, insort
from heapq import heappop, heappush
from itertools import permutations as itertoolspermutations

from helper_operations.path_operations import adjacent, cycleQ, pathQ


def binomial(k0: int, k1: int) -> int:
    """
    Returns binomial coefficient: `k0+k1 choose k0`.

    Args:
        k0 (int): The first parameter of the binomial coefficient.
        k1 (int): The second parameter of the binomial coefficient.

    Returns:
        int: The calculated binomial coefficient.

    Raises:
        AssertionError: If `k0` or `k1` is negative.
    """
    assert k0 >= 0 and k1 >= 0
    if k0 == 0:
        return 1
    elif k1 < k0:
        return binomial(k1, k0)
    else:
        k = k1 + 1
        return (binomial(k0 - 1, k) * k) // k0


def multinomial(s: list[int]) -> int:
    """
    Returns multinomial coefficient for list `s`. `s` is a list of integers, where each integer represents the number of
    occurrences of a unique element in a multiset. The multinomial coefficient is calculated as the product of the
    binomial coefficients of the elements in `s`. The multinomial coefficient is the number of ways to arrange the
    elements of a multiset.

    Args:
        s (list[int]): The list of integers for which the multinomial coefficient is calculated.

    Returns:
        int: The calculated multinomial coefficient.

    Raises:
        AssertionError: If any element in `s` is negative.
    """
    assert all(0 <= k for k in s)
    if len(s) <= 1:
        return 1
    t = sorted(s)
    k0, k1 = t[0], t[1]
    t[1] = k0 + k1
    return binomial(k0, k1) * multinomial(t[1:])


def perm(sig: list[int]) -> list[list[int]]:
    """
    Returns all permutations with signature `sig`. The signature is a list of integers, where each integer represents the
    number of occurrences of a unique element in a multiset. The permutations are returned as a list of lists of integers.

    Args:
        sig (list[int]): Signature as a list of integers

    Returns:
        list[list[int]]: List of permutations as lists of integers
    """
    first_perm = []
    for index, item in enumerate(sig):
        first_perm.extend([index] * item)

    return [list(p) for p in set(itertoolspermutations(first_perm))]


def get_num_of_inversions(permutation: tuple[int, ...]) -> int:
    """
    Count the number of inversions in a permutation using merge sort.
    See references for more information.

    Args:
        permutation (tuple[int, ...]): Permutation as a tuple of integers

    Returns:
        int: Number of inversions in the permutation

    References:
        - From https://www.geeksforgeeks.org/inversion-count-in-array-using-merge-sort/
    """
    if len(permutation) <= 1:
        return 0
    sortList = []
    result = 0
    # Heapsort, O(N*log(N))
    for i, v in enumerate(permutation):
        heappush(sortList, (v, i))
    # Create a sorted list of indexes
    x = []
    while sortList:
        # O(log(N))
        v, i = heappop(sortList)
        # Find the current minimum's index
        # the index y can represent how many minimums on the left
        y = bisect(x, i)
        # i can represent how many elements on the left
        # i - y can find how many bigger nums on the left
        result += i - y

        insort(x, i)

    return result


def count_inversions(sig: list[int]) -> dict[tuple, int]:
    """
    Count the number of inversions for all permutations of a signature

    Args:
        sig (list[int]): Signature as a list of integers

    Returns:
        dict[tuple, int]: Dictionary with permutations as keys and number of inversions as values
    """
    if len(sig) == 0:
        return dict()
    return {tuple(i): get_num_of_inversions(i) for i in perm(sig)}


def defect(s: list[int]) -> int:
    """
    Compute the defect of a signature. The defect is the difference between the number of even and odd permutations.
    The defect is the number of permutations that cannot be reached in the bipartite neighbor-swap graph.
    This defect is calculated by the difference in nodes between the two partitions of the bipartite graph.
    A bipartite graph can only admit a Hamiltonian cycle if the defect is 0 since it needs to alternate between the two partitions.

    Args:
        s (list[int]): Signature as a list of integers

    Returns:
        int: The absolute difference between the number of even and odd permutations.
    """
    if len(s) < 2:
        return 0
    inv_dict = count_inversions(s)
    even_count = sum(1 for value in inv_dict.values() if value % 2 == 0)
    return abs(even_count - (len(inv_dict) - even_count))


def swapPair(perm: tuple[int, ...], i: int, j: int = None) -> tuple[int, ...]:
    """
    Swaps elements in perm at positions `i` and `j` (or `i` and `i+1` if `j` is not provided).
    Note that `i` and `j` can be negative, in which case they are counted from the end of the permutation.

    Args:
        perm (tuple[int, ...]): Permutation as a tuple of integers.
        i (int): Index to place the element that was previously at position `j`.
        j (int, optional): Index to place the element that was previously at position `i`. Defaults to `i+1`.

    Returns:
        tuple[int, ...]: `perm` with elements at positions `i` and `j` swapped.

    Raises:
        ValueError: If the index `i` or `j` is out of range for the given permutation.
    """
    perm = list(perm)
    if j is None:
        j = i + 1
    if i > len(perm) - 1 or j > len(perm) - 1:
        raise ValueError(f"Index {i} out of range for permutation {perm}")
    if i < len(perm) and j < len(perm):
        perm[i], perm[j] = perm[j], perm[i]
    return tuple(perm)


def generate_adj(p: list[int]) -> list[tuple[int, ...]]:
    """
    Returns all adjacent elements of permutation `p`. Adjacent elements are generated by swapping pairs of elements in `p`.

    Args:
        p (list[int]): List of integers representing a permutation

    Returns:
        list[tuple[int, ...]]: List of tuples representing the new permutations generated by neighbor-swapping
    """
    v = []
    for i, item in enumerate(p):
        if i + 1 < len(p) and item != p[i + 1]:
            v.append(swapPair(p, i))
    return v


def graph(sig: list[int]) -> dict[str, set[str]]:
    """
    Returns a graph with signature `sig` in form of dictionary of strings.
    Generates an adjacency dictionary where the keys are permutations and the values are sets of adjacent permutations.

    Args:
        sig (list[int]): signature as a list of integers

    Returns:
        dict[str, set[str]]: dictionary with permutations as keys and adjacent permutations as values
    """
    if len(sig) == 0:
        return dict()
    p = perm(sig)

    dic = {}
    for i in p:
        dic["".join(map(str, i))] = set(
            ["".join(map(str, el)) for el in generate_adj(i)]
        )
    return dic


def extend(lst: list[tuple[int, ...]], e: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Extend every item in `lst` with `e`. The extension is done by concatenating the tuple `e` to each tuple in `lst`.

    Args:
        lst (list[tuple[int, ...]]): List of tuples to be extended.
        e (tuple[int, ...]): Tuple to extend every item in `lst` with.

    Returns:
        list[tuple[int, ...]]: List of tuples with each item extended by `e`.
    """
    return [i + e for i in lst]


def extend_cycle_cover(
    lis3d: list[list[tuple[int, ...]]], e: tuple[int, ...]
) -> list[list[tuple[int, ...]]]:
    """
    Extend every item in a list of unknown depth holding a list of permutations with `e`.

    Args:
        lis3d (list[list[tuple[int, ...]]]): List of unknown depth with list of tuples.
        e (tuple[int, ...]): Tuple to extend every item in `lis3d` with.

    Returns:
        list[list[tuple[int, ...]]]: List of extended permutations. The list structure is preserved.
    """
    assert len(lis3d) > 0
    if isinstance(lis3d[0][0][0], int):
        return [extend(l, e) for l in lis3d]
    elif not isinstance(lis3d, list):
        raise ValueError("The input is not a list")
    else:
        return [extend_cycle_cover(l, e) for l in lis3d]


def shorten(lis: list[tuple[int, ...]], num: int) -> list[tuple[int, ...]]:
    """
    Shorten every item in `l` by `num` elements from the end.

    Args:
        lis (list[tuple[int, ...]]): List of permutations
        num (int): Number of elements to remove from the back

    Returns:
        list[tuple[int, ...]]: List of shortened permutations.
    """
    assert len(lis) > 0
    assert all(len(i) >= num for i in lis)
    if num == 0:
        return lis
    if num < 0:
        return [i[-num:] for i in lis]
    return [i[:-num] for i in lis]


def signature(permutation: tuple[int, ...]) -> list[int]:
    """
    Returns the signature of a permutation.

    Args:
        permutation (tuple[int, ...]): The permutation as a tuple of integers.

    Returns:
        list[int]: The signature of the permutation as a list of integers.
    """
    if not permutation:
        return []
    return [permutation.count(i) for i in range(max(permutation) + 1)]


def rotate(l: list, n: int) -> list:
    """
    Rotates the list `l` by `n` positions to the **left**.

    Args:
        l (list): The list to rotate.
        n (int): The number of positions to rotate.

    Returns:
        list: The rotated list.
    """
    if len(l) <= 1:
        return l
    return l[n % len(l) :] + l[: n % len(l)]


def halve_signature(sig: list[int]) -> list[int]:
    """
    Halves a signature `sig` (list of integers) by taking every element and dividing it by 2. The result is rounded down.

    Args:
        sig (list[int]): Signature as a list of integers.

    Returns:
        list[int]: Halved signature as a list of integers.

    Raises:
        ValueError: If the signature contains negative integers.

    Examples:
        >>> _halveSignature([2, 4, 6])
        [1, 2, 3]
        >>> _halveSignature([1, 3, 5])
        [0, 1, 2]
    """
    if any(i < 0 for i in sig):
        raise ValueError("Signature must be a list of non-negative integers.")
    return [i // 2 for i in sig]


def multiset(s: list[int]) -> tuple[int, ...]:
    """
    Generates the lexicographically smallest list with given signature.

    Args:
        s (list[int]): List of integers, each representing the frequency of the corresponding element (signature).

    Returns:
        tuple[int, ...]: Lexicographically smallest permutation with the given signature.
    """
    if isinstance(s, int):
        s = [s]
    if not all(i >= 0 for i in s):
        raise ValueError("Signature must be a list of non-negative integers.")
    return tuple([i for i, f in enumerate(s) for _ in range(f)])


def permutations_from_sig(sig: list[int]) -> list[tuple[int, ...]]:
    """
    Generates all possible permutations of a given signature `sig` which is list of integers.

    Args:
        sig (list[int]): List of integers, the signature.

    Returns:
        list[tuple[int, ...]]: List of permutations as tuples of integers.
    """
    if isinstance(sig, int):
        sig = [sig]
    if len(sig) == 0:
        return []
    # for itertools permutations:
    # Elements are treated as unique based on their position, not on their value.
    return list(set(itertoolspermutations(multiset(sig))))


def _selectOdds(sig: tuple[int, ...]) -> tuple[int, ...]:
    """
    Returns only the odd occurences of colors in the given signature `sig`.

    Args:
        sig (tuple[int, ...]): The signature as a tuple of integers.

    Returns:
        tuple[int, ...]: A tuple of integers with odd occurrence frequencies.
    """
    return tuple([i for i, item in enumerate(sig) if item % 2 == 1])


def stutterPermutations(s: list[int]) -> list[tuple[int, ...]]:
    """
    Generates stutter permutations of a given signature.
    A stutter permutation is a permutation where each element is repeated twice.
    It can have a single trailing element but no other odd elements.
    If the signature is empty or contains only a single 0, an empty list is returned.

    Args:
        s (list[int]): Signature of the permutations as a list of integers.

    Returns:
        list[tuple[int, ...]]: Stutter permutations as a list of tuples of integers.
    """
    odds = _selectOdds(s)
    if len(odds) >= 2 or len(s) == 0 or (len(s) == 1 and s[0] == 0):
        return []
    else:
        result = _stutterize(permutations_from_sig(halve_signature(s)))
        if len(odds) == 1:
            return extend(result, odds)
        else:
            return result


def nonStutterPermutations(s: list[int]) -> list[tuple[int, ...]]:
    """
    Returns all non-stutter permutations of signature `sig`.
    See `stutterPermutations` for the definition of stutter permutations.

    Args:
        s (list[int]): signature of the permutations as a list of integers

    Returns:
        list[tuple[int, ...]]: non-stutter permutations as a list of tuples of integers
    """
    if len(s) == 0 or (len(s) == 1 and s[0] == 0):
        return []
    return [tuple(p) for p in perm(s) if not tuple(p) in stutterPermutations(s)]


def _stutterize(p_list: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """
    Converts a list of permutations into stutter permutation by repeating every number twice

    Args:
        p_list (list[tuple[int, ...]]): A list of permutations as a list of tuples of integers

    Returns:
        list[tuple[int, ...]]: All stutter permutations as a list of tuples of integers
    """
    return [tuple([el for el in t for _ in range(2)]) for t in p_list]


def selectByTail(
    permutations: list[tuple[int, ...]], tail: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """
    Select permutations with a given tail 'tail'

    Args:
        permutations (list[tuple[int, ...]]): List of permutations
        tail (tuple[int, ...]): Elements of the tail to select

    Returns:
        list[tuple[int, ...]]: List of permutations with the given tail

    Raises:
        AssertionError: If the length of the permutations differs between the permutations.
    """
    assert all(len(i) == len(permutations[0]) for i in permutations)
    return [i for i in permutations if i[-len(tail) :] == tail]


def HpathQ(per: list[tuple[int, ...]], sig: list[int]) -> bool:
    """
    Determines whether the path is a Hamiltonian path on the non-stutter permutations of the given signature.
    The list is a Hamiltonian path iff it is a path **and** the set of permutations is equal to the set of non-stutter permutations.

    Args:
        per (list[tuple[int, ...]]): List of permutations ordered in a path.
        sig (list[int]): Signature as a list of integers.

    Returns:
        bool: `True` if the path is a Hamiltonian path on the non-stutter permutations of the given signature, `False` otherwise.
    """
    if pathQ(per):
        return set(per) == set(nonStutterPermutations(sig))
    return False


def HcycleQ(per: list[tuple[int, ...]], sig: list[int]) -> bool:
    """
    Determines whether the list of permutations is a Hamiltonian cycle on the non-stutter permutations of the given signature.
    The list is a Hamiltonian cycle iff the list is a Hamiltonian path **and** the first and last permutations are adjacent.

    Args:
        per (list[tuple[int, ...]]): List of permutations, ordered in a cycle.
        sig (list[int]): Signature as a list of integers.

    Returns:
        bool: `True` if the list of permutations is a Hamiltonian cycle on the non-stutter permutations of the given signature, `False` otherwise.
    """
    if len(per) <= 2:
        return False
    return adjacent(per[0], per[-1]) and HpathQ(per, sig)


def LargeHpathQ(per: list[tuple[int, ...]], sig: list[int]) -> bool:
    """
    Determines whether the list is a Hamiltonian path on the non-stutter permutations of the given signature.
    Used for "larger" signatures where the path contains a lot of permutations. The other function will get slow
    then because it has to compare all permutations. This only only checks properties for a Hamiltonian path:\n
    - No duplicates\n
    - Correct length\n
    - Is a path\n

    Args:
        per (list[tuple[int, ...]]): List of permutations, ordered in a path.
        sig (list[int]): Signature as a list of integers.

    Returns:
        bool: `True` if the path is a Hamiltonian path on the non-stutter permutations of the given signature, `False` otherwise.
    """
    # there are no duplicates, the length is correct, and it is a path
    if len(per) <= 2:
        return False
    # there are no duplicates, the length is correct, and it is a cycle
    if sum(1 for n in sig if n % 2 == 1) < 2:
        expected_length = multinomial(sig) - len(nonStutterPermutations(sig))
    else:
        expected_length = multinomial(sig)
    return len(set(per)) == len(per) and len(per) == expected_length and pathQ(per)


def LargeHcycleQ(per: list[tuple[int, ...]], sig: list[int]) -> bool:
    """
    Determines whether the list is a Hamiltonian cycle on the non-stutter permutations of the given signature.
    Used for "larger" signatures where the cycle contains a lot of permutations. The other function will get slow
    then because it has to compare all permutations. This only only checks properties for a Hamiltonian cycle:\n
    - No duplicates\n
    - Correct length\n
    - Is a cycle\n

    Args:
        per (list[tuple[int, ...]]): List of permutations, ordered in a cycle.
        sig (list[int]): Signature as a list of integers.

    Returns:
        bool: `True` if the list is a Hamiltonian cycle on the non-stutter permutations of the given signature, `False` otherwise.
    """
    if len(per) <= 2:
        return False
    # there are no duplicates, the length is correct, and it is a cycle
    if sum(1 for n in sig if n % 2 == 1) < 2:
        expected_length = multinomial(sig) - len(nonStutterPermutations(sig))
    else:
        expected_length = multinomial(sig)
    return len(set(per)) == len(per) and len(per) == expected_length and cycleQ(per)


def total_path_motion(permutation_list: list[tuple[int, ...]]) -> int:
    """
    Returns the sum of the transposition widths for all edges in the permutation_list.
    The difference in index between the two transposed elements is the width of the transposition.
    The total motion is the sum of all transposition widths in the permutation_list.
    Note that the list is not required to be a path because the function takes into account the transpositions widths.

    Args:
        permutation_list (list[tuple[int, ...]]): List of permutations to calculate the total motion for

    Returns:
        int: Total motion as an integer
    """
    total_motion = 0
    for node in range(len(permutation_list) - 1):
        permutation_a = permutation_list[node]
        permutation_b = permutation_list[node + 1]
        for i in range(len(permutation_a)):
            if permutation_a[i] != permutation_b[i]:
                for j in range(i, len(permutation_a)):
                    if permutation_a[j] != permutation_b[j]:
                        width = abs(i - j)
                        if width > 2:
                            print(
                                f"Width of transposition {node} is {width}: {permutation_a}, {permutation_b}"
                            )
                        total_motion += width
    return total_motion
