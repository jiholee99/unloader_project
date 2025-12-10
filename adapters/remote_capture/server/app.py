#!/usr/bin/env python3
"""
Flask server for handling slave synchronization and file uploads
"""
from flask import Flask, request, jsonify
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename
import threading
import os

from utils.logger import get_logger

class Server:
    def __init__(self, upload_base_dir="/home/lgvision/Pictures/slave_uploads"):
        self.logger = get_logger()
        self.app = Flask(__name__)
        self.upload_base_dir = upload_base_dir
        
        # Ensure base upload directory exists
        os.makedirs(self.upload_base_dir, exist_ok=True)
        
        # Dictionary holding the state of each slave
        self.slave_signals = {
            "slave1": False,
            "slave2": False
        }
        
        # ---------------- Routes ----------------
        
        @self.app.route("/signal", methods=["GET", "POST"])
        def signal():
            if request.method == "POST":
                data = request.get_json()
                for k in self.slave_signals.keys():
                    if k in data:
                        self.slave_signals[k] = data[k]
                return jsonify(self.slave_signals)
            # GET returns current slave signals
            return jsonify(self.slave_signals)
        
        @self.app.route("/signal/reset/<slave_id>", methods=["POST"])
        def reset(slave_id):
            if slave_id in self.slave_signals:
                self.slave_signals[slave_id] = False
            return jsonify({"status": "reset", "slave": slave_id})
        
        # *** THIS IS THE CRITICAL MISSING ROUTE ***
        @self.app.route("/upload/<slave_id>", methods=["POST"])
        def upload(slave_id):
            """Handle file uploads from slaves"""
            try:
                if 'file' not in request.files:
                    self.logger.error(f"[{slave_id}] Upload failed: No file in request")
                    # print(f"[{slave_id}] Upload failed: No file in request")
                    return jsonify({"error": "No file part"}), 400
                
                file = request.files['file']
                if file.filename == '':
                    self.logger.error(f"[{slave_id}] Upload failed: Empty filename")
                    # print(f"[{slave_id}] Upload failed: Empty filename")
                    return jsonify({"error": "No selected file"}), 400
                
                # Create slave directory if it doesn't exist
                slave_dir = os.path.join(self.upload_base_dir, slave_id)
                os.makedirs(slave_dir, exist_ok=True)
                
                # Save the file
                filename = secure_filename(file.filename)
                filepath = os.path.join(slave_dir, filename)
                file.save(filepath)
                
                self.logger.info(f"[{slave_id}] Received and saved: {filename} -> {filepath}")
                # print(f"✓ [{slave_id}] Received and saved: {filename} -> {filepath}")
                return jsonify({
                    "status": "success", 
                    "filename": filename, 
                    "path": filepath
                })
                
            except Exception as e:
                self.logger.error(f"[{slave_id}] Upload error: {e}")
                # print(f"✗ [{slave_id}] Upload error: {e}")
                return jsonify({"error": str(e)}), 500
        
        # --------------------------------------
        self.server = None
        self.thread = None
    
    def start(self):
        if self.server is not None:
            self.logger.error("Server already running!")
            # print("⚠ Server already running!")
            return
        self.server = make_server("0.0.0.0", 5000, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info("Server started on 0.0.0.0:5000")
        # print("✓ Server started on 0.0.0.0:5000")
    
    def stop(self):
        if self.server is None:
            self.logger.error("Server is not running!")
            # print("⚠ Server is not running!")
            return
        self.server.shutdown()
        self.thread.join()
        self.server = None
        self.thread = None
        self.logger.info("Server stopped.")
        # print("✓ Server stopped.")


# Test the server standalone
if __name__ == "__main__":
    server = Server()
    server.start()
    
    try:
        print("\nServer running. Press Ctrl+C to stop...\n")
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()
