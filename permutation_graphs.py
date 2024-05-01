from itertools import chain, permutations as itertoolspermutations
from collections import Counter
import math
from path_operations import cycleQ, pathQ
from typing import List, Dict


def binomial(k0: int, k1: int) -> int:
    """Returns binomial coefficient k0+k1 choose k0, which equals k0+k1 choose k1.
        Assumption: 0 <= k0 and 0 <= k1
    """
    if k0 == 0:
        return 1
    elif k1 < k0:
        return binomial(k1, k0)
    else:
        k = k1 + 1
        return (binomial(k0-1, k) * k) // k0


def multinomial(s: List[int]) -> int:
    """Returns multinomial coefficient for list s.
        Assumption: all(0 <= k for k in s)"""
    if len(s) <= 1:
        return 1
    t = sorted(s)
    k0, k1 = t[0], t[1]
    t[1] = k0 + k1
    return binomial(k0, k1) * multinomial(t[1:])


def perm(sig) -> List[list]:
    """Returns all permutations with signature sig"""
    first_perm = []
    for index, item in enumerate(sig):
        first_perm.extend([index] * item)

    return [list(p) for p in set(itertoolspermutations(first_perm))]


def start_perm(sig) -> tuple:
    """Returns the permutation of the least serial number"""
    return tuple(sum([[i] * count for i, count in enumerate(sig)], []))


def non_stutters(sig) -> List[tuple]:
    """"Returns all non-Stutters permutations of signature sig"""
    return [tuple(p) for p in perm(sig) if not stutterPermutationQ(p)]


def stutters_sig(sig) -> list:
    """Returns all Stutters permutations of signature sig"""
    return [i for i in perm(sig) if stutterPermutationQ(i)]


def stutters_perm(s) -> list:
    """Returns all stutters permutations from set s of permutations?"""
    return [p for p in s if stutterPermutationQ(p)]


def defect(s) -> int:
    """
    Returns the number of spurs of a given signature according to Lehmer's definition for the defect:
    The number of even permutations - number of odd permutations
    """
    inv_dict = count_inversions(s)
    even_count = sum(1 for value in inv_dict.values() if value % 2 == 0)
    return even_count - (len(inv_dict) - even_count) - 1


def count_inversions(sig) -> Dict[tuple, int]:
    """
    Count the number of inversions for all permutations of a signature
    """
    p = perm(sig)
    dic = {}
    for i in p:
        inversions = 0
        for j in range(len(i)):
            for k in range(j + 1, len(i)):
                if i[j] > i[k]:
                    inversions += 1
        dic[tuple(i)] = inversions
    return dic


def generate_adj(s) -> List[tuple]:
    """Returns all adjacent elts of element s"""
    v = []
    for i, item in enumerate(s):
        if i + 1 < len(s) and item != s[i + 1]:
            v.append(tuple(swapPair(s, i)))
    return v


def graph(sig) -> Dict[tuple, List[tuple]]:
    """Returns a graph with signature sig in form of dictionary"""
    p = perm(sig)
    dic = {}
    for i in p:
        dic[tuple(i)] = generate_adj(i)
    return dic


def graph_stutter_free(sig):
    """Returns a graph with signature sig in form of dictionary on non stutter permutations"""
    p = perm(sig)
    dic = {}
    val = []
    for i in p:
        if not stutterPermutationQ(i):
            for j in generate_adj(i):
                if not stutterPermutationQ(j):
                    val.append(list(j))
            dic[tuple(i)] = val
            val = []
    return dic


def mul(sez, e):
    """Adds 'e' to all elements(lists) in list sez"""
    if not sez:
        return [e]
    for i in sez:
        i.append(e)
    return sez


def mult(sez, e):
    """"Adds 'e' to all elements(tuples) in list sez"""
    for i in sez:
        i += (e,)
    return sez


def Mul(dic, e):
    """Adds 'e' to dictionary dic (to keys and values)"""
    for i in list(dic.keys()):
        for j in dic[i]:
            j.append(e)
        dic[i + (e,)] = dic.pop(i)
    return dic


def multiset(s):
    """Tried with return [] but got list of lists so did it like this:"""
    per = []
    for i, item in enumerate(s):
        per.extend(item * [i])
    return per


def extend(lst: list, e: tuple):
    """
     Extend every item in l with e
    :param lst: list of tuples
    :param e: tuple to extend every item in l with
    :return:
    """
    try:
        return [i + e for i in lst]
    except TypeError:
        return [i + [e] for i in lst]


def shorten(lis, num):
    return [i[:-num] for i in lis]


def signature(s):
    """Returns signature of element s"""
    if not s:
        return []
    return [s.count(i) for i in range(max(s) + 1)]


def swapPair(perm, i, j=None):
    """Swaps elements in perm at positions i and j (or i and i+1 if j is not provided)."""
    perm = list(perm)
    if j is None:
        j = i + 1
    if i != 0 and j != 0 and i < len(perm) and j < len(perm):
        perm[i], perm[j] = perm[j], perm[i]
    return tuple(perm)


def edgeIndex(e, f):
    return [i for i, (a, b) in enumerate(zip(e, f)) if a != b][0]


def rotate(l, n):
    """Rotates the list l by n positions."""
    return l[n % len(l):] + l[:n % len(l)]


def halveSignature(sig):
    """Halves the signature. ([2, 4, 6] --> [1, 2, 3]), rounding down."""
    return [i // 2 for i in sig]


def multiset(freq):
    """Generates the lexicographically smallest list with given occurrence frequencies."""
    if isinstance(freq, int):
        freq = [freq]
    return [i for i, f in enumerate(freq) for _ in range(f)]


def permutations(s):
    """Generates all possible permutations of a given list of integers."""
    if isinstance(s, int):
        s = [s]
    # for itertools permutations:
    # Elements are treated as unique based on their position, not on their value.
    return list(set(itertoolspermutations(multiset(s))))


def stutterPermutations(s):
    """Generates stutter permutations of a given list of integers."""
    odds = selectOdds(s)
    if len(odds) >= 2:
        return []
    else:
        result = stutterize(permutations(halveSignature(s)))
        if len(odds) == 1:
            return extend(result, odds)
        else:
            return result


def stutterCounter(sig):
    #NO TESTS!
    """Returns the number of stutter permutations in a graph with signature sig."""
    return len(stutters_sig(sig))


def nonStutterCount(sig):
    #NO TESTS!
    """Returns the number of non-stutter permutations in a graph with signature sig."""
    return len(non_stutters(sig))


def stutterize(s):
    """Converts argument into stutter permutation by repeating every number."""
    return [tuple([el for el in t for _ in range(2)]) for t in s]


def selectOdds(sig):
    """Returns list of numbers with odd occurrence frequencies in the given signature."""
    return [i for i, item in enumerate(sig) if item % 2 == 1]


def selectByTail(s, tail):
    """Select permutations with a given tail 'tail'"""
    return [i for i in s if i[-len(tail):] == tail]


def stutterPermutationQ(s):
    #NO TESTS!
    """Returns true if list/tuple is stutters, false otherwise"""
    if len(s) == 1:
        return False
    for i in range(len(s) // 2):
        if s[2 * i] != s[2 * i + 1]:
            return False
    return True


def HpathQ(per, sig):
    """Determines whether the path is a Hamiltonian path on the non-stutter permutations of the given signature."""
    if pathQ(per):
        for i in non_stutters(sig):
            try:
                per.remove(i)
            except ValueError:
                return False
        if not per:
            return True
    return False


def HcycleQ(per, sig):
    """Determines whether the path is a Hamiltonian cycle on the non-stutter permutations of the given signature."""
    if cycleQ(per):
        return HpathQ(per, sig)
    else:
        return False


def transform(lis, tr):
    """Transforms the permutation(s) according to the given renaming."""

    l = []
    for i in lis:
        v = []
        for j in i:
            try:
                v.append(tr[j])
            except IndexError:
                return "list of transformations is too short"
        l.append(v)
    return l


def conditionHpath(sig):
    """Condition for existence of Hamiltonian path on all permutations of the given signature."""
    if len(sig) == 1:
        return True
    if len(sig) == 2 and sig[0] == 1 or sig[1] == 1:
        return True
    st = 0
    for i in sig:
        if i % 2 == 1:
            st += 1
    if st >= 2:
        return True
    return False


def conditionHcycle(sig):
    """Condition for existence of Hamiltonian cycle on all permutations of the given signature."""
    if len(sig) < 2:
        return False
    st = 0
    for i in sig:
        if i % 2 == 1:
            st += 1
    if st >= 2:
        if len(sig) == 3:
            try:
                sig.remove(1)
                sig.remove(1)
                if sig[0] % 2 == 0:
                    return False
            except ValueError:
                return True
        return True
    return False


def conditionHpathNS(sig):
    # For every neighbor-swap graph, the subgraph consisting of its non-stutter permutations admits a Hpath
    return True


def conditionHcycleNS(sig):
    """Condition for existence of Hamiltonian cycle on all non-stutter permutations of the given signature."""
    if len(sig) < 2:
        return False
    if len(sig) == 2 and (sig[0] % 2 == 1 or sig[1] % 2 == 1):
        return False
    if len(sig) == 3:
        try:
            sig.remove(1)
            sig.remove(1)
            if sig[0] % 2 == 0:
                return False
        except ValueError:
            return True
    return True


def total_path_motion(path):
    """
     Returns the sum of the widths (difference in index between the two transposed elements) for all nodes in the path
    """
    total_motion = 0
    for node in range(len(path) - 1):
        permutation_a = path[node]
        permutation_b = path[node + 1]
        for i in range(len(permutation_a)):
            if permutation_a[i] != permutation_b[i]:
                for j in range(i, len(permutation_a)):
                    if permutation_a[j] != permutation_b[j]:
                        width = abs(i - j)
                        if width > 2:
                            print(f"Width of transposition {node} is {width}: {permutation_a}, {permutation_b}")
                        total_motion += width
    print(path)
    return total_motion
