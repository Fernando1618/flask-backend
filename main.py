from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "API funcionando correctamente"}), 200

@app.route("/api/mensaje", methods=["POST"])
def mensaje():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    return jsonify({"respuesta": f"Mensaje recibido: {mensaje}"}), 200

if __name__ == "__main__":
    app.run(debug=True) 
