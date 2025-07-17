from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/mensaje', methods=['POST'])
def handle_message():
    data = request.json
    comando = data.get('comando')
    
    if comando == 'ping':
        return jsonify({"status": "ok"})
    
    # Aquí procesar otros comandos...
    return jsonify({"status": "received", "comando": comando})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
