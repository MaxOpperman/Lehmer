def validate_signature(signature):
    """
    Validate the input signature.

    Args:
        signature (tuple[int, ...]): The input signature to validate.

    Raises:
        ValueError: If the signature is not a list or tuple, or if it contains non-negative integers.
    """
    if not isinstance(signature, (list, tuple)):
        raise ValueError("Signature must be a list or tuple.")
    if not all(isinstance(x, int) and x >= 0 for x in signature):
        raise ValueError("Signature must contain non-negative integers.")


from core.cycle_cover import get_connected_cycle_cover
from core.helper_operations.cycle_cover_connections import (
    generate_end_tuple_order,
    get_cross_edges,
)


def case_one_to_eight_cross_edges(signature):
    """
    For certain signatures, return True if the signature matches any of the specified cases.

    Args:
        signature (tuple[int, ...]): The input signature to check.
    Returns:
        bool: True if the signature matches any of the specified cases (1 up to and including 8), False otherwise.
    """
    sig = tuple(signature)
    length = len(sig)

    # Case 0: length <= 2
    if length <= 2:
        print("Matched Case 0: length <= 2")
        return True

    # Case 2: (even, 2, 1)
    if length == 3 and sig[0] % 2 == 0 and sig[1] == 2 and sig[2] == 1:
        print("Matched Case 2: (even, 2, 1)")
        return True

    # Case 3: (odd, 2, 1) with odd frequency >= 3
    if length == 3 and (
        (sig[0] % 2 == 1 and sig[1] == 2 and sig[2] == 1 and sig[0] >= 3)
        or (sig == (2, 1, 1))
    ):
        print("Matched Case 3: (odd, 2, 1) with odd frequency >= 3 or (2, 1, 1)")
        return True

    # Case 4: (even, 1, 1) (only a Hamiltonian path)
    if length == 3 and sig[0] % 2 == 0 and sig[1] == 1 and sig[2] == 1:
        print("Matched Case 4: (even, 1, 1)")
        return True

    # Case 5: (odd, odd, 1) with both odd frequencies >= 3
    # Case 1: (odd, 1, 1) is also encapsulated here
    if length == 3 and sig[0] % 2 == 1 and sig[1] % 2 == 1 and sig[2] == 1:
        print("Matched Case 5: (odd, odd, 1) or (odd, 1, 1)")
        return True

    # Case 6: (even, odd, 1) and (odd, even, 1)
    # (even frequency >= 4 and odd >= 3)
    if length == 3:
        if (
            sig[0] % 2 == 0
            and sig[1] % 2 == 1
            and sig[2] == 1
            and sig[0] >= 4
            and sig[1] >= 3
        ):
            print("Matched Case 6: (even, odd, 1) with even >= 4 and odd >= 3")
            return True
        if (
            sig[0] % 2 == 1
            and sig[1] % 2 == 0
            and sig[2] == 1
            and sig[1] >= 4
            and sig[0] >= 3
        ):
            print("Matched Case 6: (odd, even, 1) with even >= 4 and odd >= 3")
            return True

    # Case 7: (even, 1, 1, 1)
    if length == 4 and sig[0] % 2 == 0 and sig[1] == 1 and sig[2] == 1 and sig[3] == 1:
        print("Matched Case 7: (even, 1, 1, 1)")
        return True

    # Case 8: (even, 2, 1, 1)
    if length == 4 and sig[0] % 2 == 0 and sig[1] == 2 and sig[2] == 1 and sig[3] == 1:
        print("Matched Case 8: (even, 2, 1, 1)")
        return True

    print("No match for cases 1 to 8")
    # If none of the above, return False
    return False


def get_cross_edges_per_signature(signature: tuple[int, ...]) -> (
    tuple[
        list[
            tuple[
                tuple[tuple[int, ...], tuple[int, ...]],
                tuple[tuple[tuple[int, ...], tuple[int, ...]]],
            ]
        ],
        list[tuple[int, ...]],
    ]
    | None
):
    """
    Get the cross edges for a given signature.
    Args:
        signature (tuple[int, ...]): The input signature to process.
    Returns:
        tuple: A tuple containing:
            - A list of cross edges, where each edge is represented as a tuple of tuples.
            - A list of trailing numbers (end tuples).
        None: If the signature does not match any of the cases from 1 to 8.
    """
    if case_one_to_eight_cross_edges(signature):
        return None

    # Get the connected cycle cover for the signature
    trailing_numbers = generate_end_tuple_order(signature)
    cross_edges = get_cross_edges(signature, trailing_numbers)

    return cross_edges, trailing_numbers
