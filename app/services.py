from flask import jsonify

from app.utils import get_cross_edges_per_signature
from core.cycle_cover import get_connected_cycle_cover
from core.helper_operations.cycle_cover_connections import generate_end_tuple_order


def generate_cycles(signature: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """
    Generate the cycle structure for a given signature.

    Args:
        signature (tuple[int, ...]): The input signature to process.

    Returns:
        list[list[tuple[int, ...]]]: The generated cycle structure.
    """
    return get_connected_cycle_cover(signature)


def get_end_tuple_order(signature: tuple[int, ...]) -> list[tuple[int, ...]]:
    """
    Get the order of end tuples in the cycle cover.

    Args:
        signature (tuple[int, ...]): The input signature to process.

    Returns:
        list[tuple[int, ...]]: The order of end tuples.
    """
    return generate_end_tuple_order(signature)


def cross_edges_service(signature: tuple[int, ...]) -> (
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
    Service to get cross edges for a given signature.

    Args:
        signature (tuple[int, ...]): The input signature to process.

    Returns:
        tuple[list[tuple[tuple[tuple[int, ...], tuple[int, ...]], tuple[tuple[tuple[int, ...], tuple[int, ...]]]]], list[tuple[int, ...]]] | None:
            A tuple containing a list of cross edges and a list of trailing numbers (end tuples),
            or None if the signature does not match any cases.
    """

    result = get_cross_edges_per_signature(signature)
    if result is None:
        return (
            jsonify(
                {"error": f"Signature {signature} not supported for visualization."}
            ),
            400,
        )

    cross_edges, trailing_numbers = result

    # Build nodes and edges for the frontend
    nodes = [
        {
            "id": idx,
            "trailing": trailing[1:],
            # "signature": signature,
            "subsignature": tuple(
                signature[i] - sum(1 for t in trailing[1:] if i == t)
                for i in range(len(signature))
            ),
        }
        for idx, trailing in enumerate(trailing_numbers)
    ]

    # Convert cross_edges keys from tuple to string for frontend compatibility
    cross_edges_str_keys = {
        str([list(k[0][1:]), list(k[1][1:])]): v for k, v in cross_edges.items()
    }

    return {
        "nodes": nodes,
        "edges": cross_edges_str_keys,
    }
