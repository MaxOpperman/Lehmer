from flask import Flask, jsonify, request

from core.cycle_cover import get_connected_cycle_cover

app = Flask(__name__)


@app.route("/generate_cycles", methods=["POST"])
def generate_cycles():
    data = request.json
    signature = tuple(data.get("signature", []))
    if not signature:
        return jsonify({"error": "Invalid signature"}), 400

    # Generate the cycle structure
    try:
        cycles = get_connected_cycle_cover(signature)
        print("Generated cycles:", cycles)  # Debugging
        return jsonify({"cycles": cycles})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/subcycle", methods=["POST"])
def get_subcycle():
    data = request.json
    sub_signature = tuple(data.get("sub_signature", []))
    if not sub_signature:
        return jsonify({"error": "Invalid sub-signature"}), 400

    # Generate subcycle details
    try:
        subcycle = get_connected_cycle_cover(sub_signature)
        return jsonify({"subcycle": subcycle})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
