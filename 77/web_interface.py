from flask import Flask, jsonify

def show_web_interface():
    app = Flask(__name__)

    @app.route('/status', methods=['GET'])
    def get_status():
        return jsonify({"status": "running"})

    app.run(host='0.0.0.0', port=5000)
