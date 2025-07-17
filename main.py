from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Almacenamiento para comunicación bidireccional
ultimo_comando_hmi = ""
ultima_respuesta_esp = ""

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API operativa"})

# Ruta para que el HMI envíe comandos
@app.route("/api/hmi/comando", methods=["POST"])
def recibir_comando_hmi():
    global ultimo_comando_hmi
    data = request.get_json()
    
    if not data or "comando" not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    ultimo_comando_hmi = data["comando"]
    return jsonify({"status": "ok", "comando_recibido": ultimo_comando_hmi})

# Ruta para que el ESP32 obtenga comandos
@app.route("/api/esp32/obtener-comando", methods=["GET"])
def obtener_comando_esp32():
    return jsonify({"comando": ultimo_comando_hmi})

# Ruta para que el ESP32 envíe respuestas
@app.route("/api/esp32/respuesta", methods=["POST"])
def recibir_respuesta_esp32():
    global ultima_respuesta_esp
    data = request.get_json()
    
    if not data or "respuesta" not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    ultima_respuesta_esp = data["respuesta"]
    return jsonify({"status": "ok", "respuesta_recibida": ultima_respuesta_esp})

# Ruta para que el HMI obtenga respuestas
@app.route("/api/hmi/obtener-respuesta", methods=["GET"])
def obtener_respuesta_hmi():
    return jsonify({"respuesta": ultima_respuesta_esp})
