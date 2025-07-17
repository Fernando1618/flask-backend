from flask import Flask, request, jsonify
import serial  # <-- Añade esta importación
import time

app = Flask(__name__)

# Configuración del puerto serial (ajusta según tu configuración)
SERIAL_PORT = '/dev/ttyUSB0'  # Puede variar según tu sistema
BAUD_RATE = 115200

@app.route('/api/mensaje', methods=['POST'])
def handle_message():
    data = request.json
    comando = data.get('comando', '').upper().strip()  # Convertir a mayúsculas y limpiar
    
    if not comando:
        return jsonify({"status": "error", "error": "Comando vacío"}), 400
    
    if comando.startswith(('G00', 'G01', 'G28', 'G90', 'G91')):
        try:
            # Configuración de conexión serial
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                ser.write(f"{comando}\n".encode())
                time.sleep(0.1)  # Pequeña pausa para asegurar envío
                
                # Opcional: Leer respuesta
                respuesta = ser.readline().decode().strip()
                
                return jsonify({
                    "status": "success",
                    "respuesta": respuesta or "Comando enviado al motor",
                    "comando": comando
                })
                
        except serial.SerialException as e:
            return jsonify({
                "status": "error",
                "error": f"Error serial: {str(e)}",
                "sugerencia": f"Verifica el puerto {SERIAL_PORT} y conexión"
            }), 500
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    return jsonify({"status": "received", "comando": comando})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
