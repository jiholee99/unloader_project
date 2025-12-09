from flask import request, jsonify
from signal_store import signal_store
from upload_handler import save_uploaded_file

def register_routes(app):

    # Master POSTs full dict: { "slave1": true, "slave2": false }
    @app.route("/signal", methods=["POST"])
    def set_signal():
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Payload must be a dictionary"}), 400

        print(f"[DEBUG] Master SET signals: {data}")
        signal_store.set_signals(data)

        return jsonify({"status": "ok", "received": data}), 200


    # Slaves poll here: GET /signal
    @app.route("/signal", methods=["GET"])
    def get_signal():
        current = signal_store.get_signals()
        print(f"[DEBUG] Slave GET signals: {current}")
        return jsonify(current), 200


    # Slave resets ONLY its own signal
    @app.route("/signal/reset/<slave_id>", methods=["POST"])
    def reset_signal(slave_id):
        print(f"[DEBUG] RESET request from: {slave_id}")
        signal_store.reset_signal(slave_id)
        return jsonify({"status": "reset", "slave": slave_id}), 200
    
    # Uploading slave files
    @app.route("/upload/<slave_id>", methods=["POST"])
    def upload(slave_id):
        if "file" not in request.files:
            return jsonify({"error": "Missing file"}), 400

        file = request.files["file"]
        saved_path = save_uploaded_file(file, slave_id)
        return jsonify({"status": "saved", "path": saved_path}), 200
