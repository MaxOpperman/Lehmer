import copy
import sys
from itertools import permutations as itertoolspermutations

import numpy as np

from helper_operations.path_operations import adjacent, spurBaseIndex
from helper_operations.permutation_graphs import binomial


def stutterize(perm: np.array) -> np.ndarray:
    """
    Converts argument into stutter permutation by repeating every number.

    Args:
        perm (np.array): A permutation of integers to be converted into a stutter permutation.

    Returns:
        np.ndarray: The input permutation but every integers is repeated twice.
    """
    return np.repeat(perm, 2, axis=1)


def selectOdds(sig: np.array) -> np.array:
    """
    Returns list of numbers with odd occurrence frequencies in the given signature.

    Args:
        sig (np.array): A signature of a permutation.

    Returns:
        np.array: A list of numbers with odd occurrence frequencies.
    """
    return sig[sig % 2 == 1]


def multiset(freq: np.array) -> np.ndarray:
    """
    Generates the lexicographically smallest list with given occurrence frequencies.

    Args:
        freq (np.array): A list of integers representing the occurrence frequencies of the elements.

    Returns:
        np.ndarray: A list of integers with the given occurrence frequencies.
    """
    return np.array([i for i, f in enumerate(freq) for _ in range(f)])


def permutations(s: np.array) -> np.ndarray:
    """
    Generates all possible permutations of a given list of integers.

    Args:
        s (np.array): The signature of the permutations.

    Returns:
        np.ndarray: A list of all possible permutations with the input signature.
    """
    # for itertools permutations:
    # Elements are treated as unique based on their position, not on their value.
    return np.unique(np.array(list(itertoolspermutations(multiset(s)))), axis=0)


def stutterPermutations(s: np.array) -> np.ndarray:
    """
    Generates stutter permutations of a given list of integers.

    Args:
        s (np.array): The signature of the permutations.

    Returns:
        np.ndarray: A list of all possible stutter permutations with the input signature.
    """
    odds = selectOdds(s)
    if odds.size >= 2:
        return np.array([])
    else:
        result = stutterize(permutations(np.divide(s, 2).astype(int)))
        if len(odds) == 1:
            return extend(result, odds)
        else:
            return result


def createZigZagPath(c: np.ndarray, uv: np.ndarray) -> np.ndarray:
    """
    Creates a zigzag path by combining two "parallel" copies of the given cycle.

    Args:
        c (np.ndarray): A cycle of even length.
        uv (np.ndarray): An array containing two elements [u, v] to append.

    Returns:
        np.ndarray: A cycle obtained by combining two "parallel" copies of the given cycle to form a 'square wave',
                running from cycle[[1]]v to cycle[[-1]]v. The two copies are distinguished by appending u and v.
                Also works for a path.

    Raises:
        AssertionError: If the elements in uv are not adjacent.
    """
    assert adjacent(uv[0], uv[1])
    temp = np.repeat(c, 2, axis=0)
    module = np.array([uv[0], uv[1], uv[1], uv[0]])
    return np.append(temp, module[np.arange(len(temp)) % 4], axis=1)


def cutCycle(c: np.ndarray, a: np.array) -> np.ndarray:
    """
    Splits a cycle at vertex a. Vertex a appears on first place

    Args:
        c (np.ndarray): A cycle.
        a (np.array): A vertex to split the cycle at.

    Returns:
        np.ndarray: A cycle which starts with vertex a.
    """
    # Find the index of c in a
    index = np.where(np.all(c == a, axis=1))[0][0]

    # Shift the cycle such that array a is first
    return np.roll(c, -index, axis=0)


def incorporateSpurInZigZag(path: np.ndarray, vertex_pair: np.ndarray) -> np.ndarray:
    """
    Incorporates a spur into a zigzag path.

    Args:
        path (np.ndarray): A zigzag path.
        vertex_pair (np.ndarray): A pair of vertices to incorporate into the path.

    Returns:
        np.ndarray: A zigzag path with the spur incorporated.
    """
    # Modify path to remove last e elements except for the first one
    i = spurBaseIndex(path, vertex_pair[0])
    return np.concatenate((path[: i + 1], vertex_pair, path[i + 1 :]), axis=0)


def incorporateSpursInZigZag(
    path: np.ndarray, vertices: np.ndarray, spur_suffixes: np.ndarray
) -> np.ndarray:
    """
    Incorporates a list of spurs into a zigzag path.

    Args:
        path (np.ndarray): A zigzag path.
        vertices (np.ndarray): A list of vertices to incorporate into the path.
        spur_suffixes (np.ndarray): A list of suffixes to incorporate into the path.

    Returns:
        np.ndarray: A zigzag path with the spurs incorporated.
    """
    C = np.concatenate(
        (
            np.repeat(vertices, spur_suffixes.shape[1], axis=0),
            np.tile(spur_suffixes, (vertices.shape[0], 1)),
        ),
        axis=1,
    )
    for vertex_index in range(0, len(C), 2):
        path = incorporateSpurInZigZag(path, [C[vertex_index], C[vertex_index + 1]])
    return path


def createSquareTube(path: np.ndarray, u: np.array, v: np.array) -> np.ndarray:
    """
    Creates a square tube path by interleaving the elements of the four copies of the path list.

    Args:
        path (np.ndarray): A path list.
        u (np.array): An array of one of the two elements to append.
        v (np.array): An array of one  of the two elements to append.

    Returns:
        np.ndarray: A square tube path; u and v are appended to the path list in an interleaved manner.
    """
    # interleave the elements of the four copies of the path list
    temp = np.repeat(path, 4, axis=0)
    uu = np.concatenate((u, u))
    uv = np.concatenate((u, v))
    vu = np.concatenate((v, u))
    vv = np.concatenate((v, v))
    module1 = np.array([uu, uv, vv, vu, vu, vv, uv, uu])
    module2 = np.array([uu, uv, vv, vu, vu, uu, uv, vv])

    # Combine the path with modules based on the index
    result = np.concatenate(
        (
            np.append(temp[:-8], module1[np.arange(len(temp[:-8])) % 8], axis=1),
            np.append(temp[-8:], module2[np.arange(len(temp[-8:])) % 8], axis=1),
        )
    )
    return result


def swapPair(perm: np.ndarray, i: int, j: int | None = None) -> np.ndarray:
    """
    Swaps elements in perm at positions i and j (or i and i+1 if j is not provided).

    Args:
        perm (np.ndarray): A permutation.
        i (int): The first index to swap.
        j (int | None, optional): The second index to swap. Defaults to None; in this case, i+1 is used.

    Returns:
        np.ndarray: The permutation with the elements at positions i and j swapped
    """
    if j is None:
        j = i + 1
    if i < len(perm) and j < len(perm):
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def extend(lst: np.ndarray, e: np.ndarray) -> np.ndarray:
    """
    Extend every item in l with e

    Args:
        lst (np.ndarray): A list of arrays.
        e (np.ndarray): An array to extend the list with.

    Returns:
        np.ndarray: A list of arrays with e appended to each array.
    """
    try:
        return np.array([np.concatenate((i, e)) for i in lst])
    except TypeError:
        return np.array([np.concatenate((i, [e])) for i in lst])
    except ValueError as err:
        print("Error in extend function", lst, e)
        raise err


def HpathNS(k0: int, k1: int) -> np.ndarray:
    """
    Computes a Hamiltonian path in the neighbor-swap graph on the non-stutter permutations for the given signature.
    If k0 and k1 are both even, the path is a Hamiltonian cycle.

    Args:
        k0 (int): Number of 0s in the signature.
        k1 (int): Number of 1s in the signature.

    Returns:
        np.ndarray: A Hamiltonian path in the neighbor-swap graph G(0^k_0|1^(k_1)).

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
    odd_perms = np.ndarray(shape=(0, k0 + k1), dtype=int)
    tuple_0 = np.full(k0, 0)
    tuple_1 = np.full(k1, 1)
    sys.setrecursionlimit(2500)
    if k0 == 0:
        if k1 % 2 == 0:
            return np.array([])
        return np.array([tuple_1])
    elif k1 == 0:
        if k0 % 2 == 0:
            return np.array([])
        return np.array([tuple_0])
    elif k1 == 1:
        for i in reversed(range(k0 + 1)):
            odd_perms = np.append(
                odd_perms,
                np.array([np.concatenate((tuple_0[:i], tuple_1, tuple_0[i:]))]),
                axis=0,
            )
        return np.array(odd_perms) if k0 % 2 else np.array(odd_perms[1:])
    elif k0 == 1:
        for i in reversed(range(k1 + 1)):
            odd_perms = np.append(
                odd_perms,
                np.array([np.concatenate((tuple_1[:i], tuple_0, tuple_1[i:]))]),
                axis=0,
            )
        return np.array(odd_perms) if k1 % 2 else np.array(odd_perms[1:])
    if k0 < k1:
        reverse_h_path = HpathNS(k1, k0)
        return np.where(
            reverse_h_path == 0, 1, np.where(reverse_h_path == 1, 0, reverse_h_path)
        )
    if k0 % 2 == 1 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), np.array([1]))
        p0 = extend(HpathNS(k0 - 1, k1), np.array([0]))

        return np.concatenate((p1[:-1], np.roll(p0, -1, axis=0), np.array([p1[-1]])))
    elif k0 % 2 == 0 and k1 % 2 == 1:
        p1 = extend(HpathNS(k0, k1 - 1), np.array([1]))
        p0 = extend(HpathNS(k0 - 1, k1), np.array([0]))
        v = p0[0]

        return np.concatenate(
            (
                np.array([v]),
                cutCycle(np.flipud(p1), swapPair(copy.deepcopy(v), -2)),
                p0[1:],
            )
        )
    elif k0 % 2 == 0 and k1 % 2 == 0:
        p1 = extend(HpathNS(k0, k1 - 1), np.array([1]))
        p0 = extend(HpathNS(k0 - 1, k1), np.array([0]))

        if k0 == k1:
            return np.concatenate((p1[::-1], p0[::-1]))
        return np.concatenate((p1[::-1], p0))
    else:
        p11 = HpathNS(k0, k1 - 2)
        p1101 = HpathNS(k0 - 1, k1 - 3)
        p0101 = HpathNS(k0 - 2, k1 - 2)
        if k0 == k1:
            p0001 = np.where(p1101 == 0, 1, np.where(p1101 == 1, 0, p1101))
            p00 = np.where(p11 == 0, 1, np.where(p11 == 1, 0, p11))
        else:
            p0001 = HpathNS(k0 - 3, k1 - 1)
            p00 = HpathNS(k0 - 2, k1)
        sp00 = extend(stutterPermutations(np.array([k0 - 3, k1 - 1])), np.array([0, 0]))
        sp11 = extend(stutterPermutations(np.array([k0 - 1, k1 - 3])), np.array([1, 1]))
        tube = createSquareTube(p0101[::-1], np.array([0, 1]), np.array([1, 0]))
        tube1, tube2, tube3 = tube[:3], tube[3:-2], tube[-2:]
        if len(p1101) == 0:
            suffices = np.array([[0, 1], [1, 0]], np.int32)
            c11xy = np.concatenate(
                (
                    np.repeat(sp11, suffices.shape[1], axis=0),
                    np.tile(suffices, (sp11.shape[0], 1)),
                ),
                axis=1,
            )
        else:
            ext_path = extend(
                cutCycle(p1101, np.append(p0101[0][:-1], 0)), np.array([1, 1])
            )
            p11xy = np.roll(
                createZigZagPath(ext_path, np.array([[1, 0], [0, 1]], np.int32)),
                -1,
                axis=0,
            )
            c11xy = incorporateSpursInZigZag(
                p11xy, sp11, np.array([[0, 1], [1, 0]], np.int32)
            )
        if len(p0001) == 0:
            suffices = np.array([[1, 0], [0, 1]], np.int32)
            c00xy = np.concatenate(
                (
                    np.repeat(sp00, suffices.shape[1], axis=0),
                    np.tile(suffices, (sp00.shape[0], 1)),
                ),
                axis=1,
            )
        else:
            ext_path = extend(
                cutCycle(p0001, np.append(p0101[-1][:-1], 1)), np.array([0, 0])
            )
            p00xy = np.roll(
                createZigZagPath(ext_path, np.array([[0, 1], [1, 0]], np.int32)),
                -1,
                axis=0,
            )
            c00xy = incorporateSpursInZigZag(
                p00xy, sp00, np.array([[1, 0], [0, 1]], np.int32)
            )
        if k0 - 2 < k1:
            p00 = np.flipud(p00)

        path_ham = np.concatenate(
            (
                extend(p11, np.array([1, 1])),
                tube1,
                c00xy,
                tube2,
                c11xy,
                tube3,
                extend(p00, np.array([0, 0])),
            ),
            axis=0,
        )
        return path_ham
