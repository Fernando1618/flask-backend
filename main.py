from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Variables de estado
ultimo_comando = ""
coordenadas_actuales = {"X": 0, "Y": 0, "Z": 0}

# Ruta de verificación
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "API lista"})

# Ruta para recibir comandos (compatible con tu HMI actual)
@app.route("/api/mensaje", methods=["POST"])
def recibir_comando():
    global ultimo_comando, coordenadas_actuales
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    # Compatibilidad con formato antiguo y nuevo
    comando = data.get("comando") or data.get("mensaje", "")
    
    if not comando:
        return jsonify({"error": "Comando vacío"}), 400
    
    ultimo_comando = comando
    
    # Simulación de movimiento (remover en producción real)
    if comando.lower().startswith("g01"):
        partes = comando.split()
        for parte in partes[1:]:
            if parte.upper().startswith("X"):
                coordenadas_actuales["X"] = float(parte[1:])
            elif parte.upper().startswith("Y"):
                coordenadas_actuales["Y"] = float(parte[1:])
            elif parte.upper().startswith("Z"):
                coordenadas_actuales["Z"] = float(parte[1:])
    
    return jsonify({
        "status": "ok",
        "respuesta": f"Comando '{comando}' ejecutado",
        "coordenadas": coordenadas_actuales
    })

# Ruta para obtener estado (opcional)
@app.route("/api/estado", methods=["GET"])
def obtener_estado():
    return jsonify({
        "ultimo_comando": ultimo_comando,
        "coordenadas": coordenadas_actuales,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
