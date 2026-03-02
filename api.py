from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)
messages = []

SECRET_KEY = os.getenv("SECRET_KEY", "changeme123")

@app.route("/api/message", methods=["GET"])
def get_messages():
    key = request.args.get("key")
    since = int(request.args.get("since", 0))
    if key != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    new_msgs = [m for m in messages if m["timestamp"] > since]
    return jsonify({"messages": new_msgs})

@app.route("/api/add", methods=["POST"])
def add_message():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    msg = data.get("message", "")
    messages.append({"message": msg, "timestamp": int(time.time())})
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
