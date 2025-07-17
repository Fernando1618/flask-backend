from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Variables globales para la comunicación
ultimo_comando = ""
ultima_respuesta = ""

@app.route("/")
def index():
    return jsonify({"status": "active", "message": "API funcionando"})

@app.route("/api/comando", methods=["POST"])
def recibir_comando():
    global ultimo_comando
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400
    
    comando = data.get("comando", "").strip()
    if comando:
        ultimo_comando = comando
        return jsonify({"status": "success", "comando": comando}), 200
    return jsonify({"status": "error", "message": "Empty command"}), 400

@app.route("/api/obtener-comando", methods=["GET"])
def obtener_comando():
    return jsonify({"comando": ultimo_comando}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
