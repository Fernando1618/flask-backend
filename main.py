from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/mensaje', methods=['POST'])
def handle_message():
    data = request.json
    comando = data.get('comando', '').upper()  # Convertir a mayúsculas
    
    if comando.startswith(('G00', 'G01')):
        try:
            # Enviar comando al ESP32 via serial
            ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            ser.write(f"{comando}\n".encode())
            ser.close()
            
            return jsonify({
                "status": "success",
                "respuesta": "Comando enviado al motor",
                "comando": comando
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    return jsonify({"status": "received", "comando": comando})
