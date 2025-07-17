from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento temporal en memoria (puede usar base de datos después)
comando_pendiente = None

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

@app.route("/api/comando", methods=["POST"])
def recibir_comando():
    global comando_pendiente
    data = request.get_json()
    comando = data.get("comando", "").strip()
    if comando:
        comando_pendiente = comando  # Guardamos el comando
        return jsonify({"status": "ok", "mensaje": f"Comando '{comando}' recibido"}), 200
    return jsonify({"status": "error", "mensaje": "Comando vacío"}), 400

@app.route("/api/comando-pendiente", methods=["GET"])
def enviar_comando_al_esp32():
    global comando_pendiente
    if comando_pendiente:
        comando_a_enviar = comando_pendiente
        comando_pendiente = None  # Lo marcamos como entregado
        return jsonify({"comando": comando_a_enviar}), 200
    return jsonify({"comando": ""}), 200  # Nada que enviar

if __name__ == "__main__":
    app.run(debug=True)
