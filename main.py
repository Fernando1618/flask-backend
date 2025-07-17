from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Almacenamiento para comunicación bidireccional
ultimo_comando_hmi = ""
ultima_respuesta_esp = ""
tof_values = {"ToF1": 0, "ToF2": 0, "ToF3": 0}

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API operativa"})

# Ruta compatible con tu HMI actual
@app.route("/api/mensaje", methods=["POST"])
def recibir_mensaje():
    global ultimo_comando_hmi
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    # Compatibilidad con tu HMI actual
    if "comando" in data:
        ultimo_comando_hmi = data["comando"]
        return jsonify({
            "status": "ok", 
            "respuesta": f"Comando '{ultimo_comando_hmi}' recibido"
        })
    elif "mensaje" in data:
        return jsonify({"respuesta": f"Mensaje recibido: {data['mensaje']}"})
    else:
        return jsonify({"error": "Formato no reconocido"}), 400

# Endpoint para sensores ToF que tu HMI está solicitando
@app.route("/api/tof", methods=["GET"])
def obtener_tof():
    return jsonify({
        "status": "ok",
        "tof": {
            "ToF1": tof_values["ToF1"],
            "ToF2": tof_values["ToF2"], 
            "ToF3": tof_values["ToF3"]
        }
    })

# Ruta para que el ESP32 envíe datos
@app.route("/api/esp32/datos", methods=["POST"])
def recibir_datos_esp32():
    global tof_values, ultima_respuesta_esp
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    # Actualizar valores ToF si vienen en la solicitud
    if "tof" in data:
        tof_values.update(data["tof"])
    
    if "respuesta" in data:
        ultima_respuesta_esp = data["respuesta"]
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
