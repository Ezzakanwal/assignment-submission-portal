
from flask import Flask, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

REPORT_FILE = Path(__file__).parent / "test-report.json"


@app.route("/report", methods=["POST"])
def receive_report():
    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    REPORT_FILE.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    return jsonify({
        "message": "Test report received successfully"
    }), 200


@app.route("/", methods=["GET"])
def home():
    return "Test Report Receiver is running!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
