from flask import Flask, request, jsonify

app = Flask(__name__)

# Comando global que guarda el último enviado por el HMI
ultimo_comando = ""

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

@app.route("/api/comando", methods=["POST"])
def recibir_comando():
    global ultimo_comando
    data = request.get_json()
    comando = data.get("comando", "").strip()
    if comando:
        ultimo_comando = comando
        return jsonify({"status": "ok", "mensaje": f"Comando recibido: {comando}"}), 200
    else:
        return jsonify({"status": "error", "mensaje": "Comando vacío"}), 400

@app.route("/api/comando-pendiente", methods=["GET"])
def enviar_comando():
    global ultimo_comando
    comando = ultimo_comando
    ultimo_comando = ""  # Limpiar después de entregar al ESP32
    return jsonify({"comando": comando}), 200

if __name__ == "__main__":
    app.run(debug=True)
