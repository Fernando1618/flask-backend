from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Variable global para almacenar el último comando
ultimo_comando = ""
ultima_respuesta = ""

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

# Ruta para que el HMI envíe comandos
@app.route("/api/comando", methods=["POST"])
def recibir_comando():
    global ultimo_comando
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No se recibió JSON"}), 400
    
    comando = data.get("comando", "").strip()
    if comando:
        ultimo_comando = comando
        return jsonify({
            "status": "ok",
            "message": f"Comando '{comando}' recibido correctamente"
        }), 200
    else:
        return jsonify({"status": "error", "message": "Comando vacío"}), 400

# Ruta para que la ESP32 obtenga el último comando
@app.route("/api/obtener-comando", methods=["GET"])
def obtener_comando():
    global ultimo_comando
    comando = ultimo_comando
    # No limpiamos el comando aquí para permitir múltiples lecturas
    return jsonify({
        "status": "ok",
        "comando": comando,
        "timestamp": datetime.now().isoformat()
    }), 200

# Ruta para que la ESP32 envíe respuestas
@app.route("/api/respuesta", methods=["POST"])
def recibir_respuesta():
    global ultima_respuesta
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No se recibió JSON"}), 400
    
    respuesta = data.get("respuesta", "").strip()
    if respuesta:
        ultima_respuesta = respuesta
        return jsonify({
            "status": "ok",
            "message": f"Respuesta '{respuesta}' recibida correctamente"
        }), 200
    else:
        return jsonify({"status": "error", "message": "Respuesta vacía"}), 400

# Ruta para que el HMI obtenga la última respuesta de la ESP32
@app.route("/api/obtener-respuesta", methods=["GET"])
def obtener_respuesta():
    global ultima_respuesta
    respuesta = ultima_respuesta
    # No limpiamos la respuesta aquí para permitir múltiples lecturas
    return jsonify({
        "status": "ok",
        "respuesta": respuesta,
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
