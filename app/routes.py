from flask import Blueprint, jsonify, request

from app.app import generate_cycles
from app.services import cross_edges_service
from app.utils import validate_signature

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

    result = cross_edges_service(signature)
    print("Result data:", result)
    return jsonify(result)


@routes.route("/generated_cycle", methods=["POST"])
def generated_cycle_route():
    data = request.json
    signature = tuple(data.get("signature", []))
    try:
        validate_signature(signature)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result = generate_cycles(signature)
    if result is None:
        return (
            jsonify(
                {"error": f"Signature {signature} not supported for visualization."}
            ),
            400,
        )

    return jsonify(result)
