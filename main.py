from flask import Flask, request, jsonify
from collections import deque
from datetime import datetime

app = Flask(__name__)

# Variables globales
comandos_pendientes = deque()
respuesta_esp32 = {"mensaje": "", "timestamp": ""}
datos_tof = {}

# 🔹 Ping simple
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

# 🔹 HMI → Enviar comando
@app.route("/api/mensaje", methods=["POST"])
def recibir_comando():
    data = request.get_json()
    comando = data.get("comando", "").strip()
    if comando:
        comandos_pendientes.append(comando)
        return jsonify({"respuesta": f"Comando encolado: {comando}"}), 200
    else:
        return jsonify({"error": "Comando vacío"}), 400

# 🔹 ESP32 → Pedir próximo comando
@app.route("/api/comando-pendiente", methods=["GET"])
def enviar_comando():
    if comandos_pendientes:
        comando = comandos_pendientes.popleft()
        return jsonify({"comando": comando}), 200
    else:
        return jsonify({"comando": ""}), 200

# 🔹 ESP32 → Enviar respuesta/estado
@app.route("/api/respuesta", methods=["POST"])
def recibir_respuesta():
    data = request.get_json()
    mensaje = data.get("respuesta", "").strip()
    if mensaje:
        respuesta_esp32["mensaje"] = mensaje
        respuesta_esp32["timestamp"] = datetime.now().isoformat()
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "mensaje": "Respuesta vacía"}), 400

# 🔹 HMI → Obtener última respuesta
@app.route("/api/respuesta", methods=["GET"])
def obtener_respuesta():
    return jsonify(respuesta_esp32), 200

# 🔹 ESP32 → Enviar datos ToF
@app.route("/api/tof", methods=["POST"])
def recibir_tof():
    global datos_tof
    datos = request.get_json()
    if datos:
        datos_tof = datos
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "mensaje": "Datos vacíos"}), 400

# 🔹 HMI → Obtener ToF
@app.route("/api/tof", methods=["GET"])
def enviar_tof():
    return jsonify({"tof": datos_tof}), 200

# 🔹 Diagnóstico general
@app.route("/api/status", methods=["GET"])
def estado_general():
    return jsonify({
        "pendientes": len(comandos_pendientes),
        "ultima_respuesta": respuesta_esp32,
        "tof": datos_tof
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
