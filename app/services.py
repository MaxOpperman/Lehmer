from flask import jsonify

from app.utils import get_cross_edges_per_signature
from core.cycle_cover import get_connected_cycle_cover
from core.helper_operations.cycle_cover_connections import generate_end_tuple_order
from core.verhoeff import HpathNS


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


def generate_binary_neighbor_swap_graph(signature: tuple[int, ...]) -> dict:
    """
    Generate the neighbor-swap graph for binary signatures using Verhoeff's algorithm.
    Binary signatures have exactly 2 non-zero values (e.g., (2,0,2) or (3,4)).

    Args:
        signature (tuple[int, ...]): The binary signature to process.

    Returns:
        dict: A dictionary with 'nodes' and 'edges' for frontend visualization.
    """
    print(f"Generating binary neighbor-swap graph for signature {signature}")

    # Get the two non-zero values and their positions
    non_zero_pairs = [(i, val) for i, val in enumerate(signature) if val > 0]

    if len(non_zero_pairs) != 2:
        raise ValueError(
            f"Expected binary signature with 2 non-zero values, got {signature}"
        )

    # Extract k0 and k1 for Verhoeff's algorithm
    pos0, k0 = non_zero_pairs[0]
    pos1, k1 = non_zero_pairs[1]

    # Generate Hamiltonian path using Verhoeff's binary algorithm
    binary_path = HpathNS(k0, k1)

    if not binary_path:
        return {"nodes": [], "edges": [], "is_full_graph": True}

    # Transform the binary path back to the original color scheme
    # Binary path uses 0s and 1s, we need to map them to the original positions
    def transform_binary_to_original(binary_perm):
        """Transform binary permutation (0s and 1s) to original signature positions."""
        result = [0] * len(signature)
        for val in binary_perm:
            if val == 0:
                result[pos0] = pos0
            else:
                result[pos1] = pos1
        return result

    # Actually, the binary permutation tells us the ORDER of colors, not positions
    # We need to construct the full permutation
    all_permutations = []
    for binary_perm in binary_path:
        # Create a permutation where 0s come from color pos0 and 1s from color pos1
        perm = tuple(pos0 if val == 0 else pos1 for val in binary_perm)
        all_permutations.append(perm)

    # Create nodes and edges
    all_nodes = []
    all_edges = []
    node_id_map = {}

    for idx, perm in enumerate(all_permutations):
        node_id = idx
        all_nodes.append(
            {
                "id": node_id,
                "trailing": [],
                "subsignature": signature,
                "permutation": list(perm),
            }
        )
        node_id_map[perm] = node_id

    # Generate edges by checking neighbor swaps
    for perm in all_permutations:
        current_id = node_id_map[perm]

        # Try swapping each adjacent pair
        for i in range(len(perm) - 1):
            swapped = list(perm)
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            swapped_tuple = tuple(swapped)

            # If the swapped permutation exists in our graph, add an edge
            if swapped_tuple in node_id_map:
                target_id = node_id_map[swapped_tuple]

                # Avoid duplicate edges
                if current_id < target_id:
                    all_edges.append(
                        {
                            "source": current_id,
                            "target": target_id,
                        }
                    )

    print(f"Generated binary graph: {len(all_nodes)} nodes, {len(all_edges)} edges")
    return {"nodes": all_nodes, "edges": all_edges, "is_full_graph": True}


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

    # Check if this is a binary signature (only 2 non-zero values)
    # Use Verhoeff's binary algorithm for these
    non_zero_values = [val for val in signature if val > 0]
    if len(non_zero_values) == 2:
        return generate_binary_neighbor_swap_graph(signature)

    result = get_cross_edges_per_signature(signature)
    if result is None:
        # For signatures without cross edges (cases 1-8), generate the complete neighbor-swap graph
        return generate_full_neighbor_swap_graph(signature)

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


def generate_full_neighbor_swap_graph(signature: tuple[int, ...]) -> dict:
    """
    Generate the complete neighbor-swap graph for signatures in cases 1-8.
    Uses get_connected_cycle_cover to get the Hamiltonian path/cycle.

    Args:
        signature (tuple[int, ...]): The input signature to process.

    Returns:
        dict: A dictionary with 'nodes' and 'edges' for frontend visualization.
    """
    from core.cycle_cover import get_connected_cycle_cover
    from core.helper_operations.path_operations import cycleQ

    print(f"Generating full graph for signature {signature}")

    # Get the Hamiltonian path or cycle
    path = get_connected_cycle_cover(signature)

    if not path:
        return {"nodes": [], "edges": [], "is_full_graph": True}

    # Check if it's a cycle
    is_cycle = cycleQ(path)

    # Create nodes
    all_nodes = []
    for idx, perm in enumerate(path):
        all_nodes.append(
            {
                "id": idx,
                "trailing": [],
                "subsignature": signature,
                "permutation": list(perm),
            }
        )

    # Create edges along the path
    all_edges = []
    for i in range(len(path) - 1):
        all_edges.append(
            {
                "source": i,
                "target": i + 1,
            }
        )

    # If it's a cycle, close it
    if is_cycle and len(path) > 1:
        all_edges.append(
            {
                "source": len(path) - 1,
                "target": 0,
            }
        )

    print(
        f"Total permutations: {len(all_nodes)}, edges: {len(all_edges)}, is_cycle: {is_cycle}"
    )
    return {"nodes": all_nodes, "edges": all_edges, "is_full_graph": True}
