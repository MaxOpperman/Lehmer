from flask import Blueprint, jsonify, request

from app.utils import get_cross_edges_per_signature, validate_signature

routes = Blueprint("routes", __name__)


@routes.route("/visualize_cycles", methods=["POST"])
def visualize_cycles_route():
    data = request.json
    signature = tuple(data.get("signature", []))

    # Validate the signature
    try:
        validate_signature(signature)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

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
            "trailing": trailing,
            # "signature": signature,
            "subsignature": tuple(
                signature[i] - sum(1 for t in trailing[1:] if i == t)
                for i in range(len(signature))
            ),
        }
        for idx, trailing in enumerate(trailing_numbers)
    ]

    # Convert cross_edges keys from tuple to string for frontend compatibility
    cross_edges_str_keys = {str(k): v for k, v in cross_edges.items()}

    result = {
        "nodes": nodes,
        "edges": cross_edges_str_keys,
    }
    print("Result data:", result)
    return jsonify(result)
