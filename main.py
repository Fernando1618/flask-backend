from flask import Flask, request, jsonify

app = Flask(__name__)

# Variables globales
ultimo_comando = ""
respuesta_esp32 = ""
datos_tof = {}

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

# 🔹 HMI → Enviar comando
@app.route("/api/mensaje", methods=["POST"])
def recibir_comando():
    global ultimo_comando
    data = request.get_json()
    comando = data.get("comando", "").strip()
    if comando:
        ultimo_comando = comando
        return jsonify({"respuesta": f"Comando recibido: {comando}"}), 200
    else:
        return jsonify({"error": "Comando vacío"}), 400

# 🔹 ESP32 → Pedir comando pendiente
@app.route("/api/comando-pendiente", methods=["GET"])
def enviar_comando():
    global ultimo_comando
    comando = ultimo_comando
    ultimo_comando = ""  # Limpiar después de enviar
    return jsonify({"comando": comando}), 200

# 🔹 ESP32 → Enviar respuesta o estado
@app.route("/api/respuesta", methods=["POST"])
def recibir_respuesta():
    global respuesta_esp32
    data = request.get_json()
    respuesta = data.get("respuesta", "")
    if respuesta:
        respuesta_esp32 = respuesta
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "error", "mensaje": "Respuesta vacía"}), 400

# 🔹 HMI → Consultar última respuesta
@app.route("/api/respuesta", methods=["GET"])
def obtener_respuesta():
    global respuesta_esp32
    return jsonify({"respuesta": respuesta_esp32}), 200

# 🔹 ESP32 → Enviar datos ToF
@app.route("/api/tof", methods=["POST"])
def recibir_tof():
    global datos_tof
    datos = request.get_json()
    if datos:
        datos_tof = datos
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "mensaje": "Datos vacíos"}), 400

# 🔹 HMI → Obtener datos ToF
@app.route("/api/tof", methods=["GET"])
def enviar_tof():
    global datos_tof
    return jsonify({"tof": datos_tof}), 200

if __name__ == "__main__":
    app.run(debug=True)
