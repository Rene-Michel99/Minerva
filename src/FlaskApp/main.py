import json
import signal
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

import sys
import os

# Obtém o caminho do diretório atual do script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Adiciona o diretório pai ao sys.path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from FlaskApp import ZeroMQClient


class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        self.zeroMQClient = ZeroMQClient()

        self.app.route("/inference", methods=["POST"])(self.api_inference)
        self.app.route("/review", methods=["POST"])(self.api_review)
        
        signal.signal(signal.SIGTERM, self.handle_sigterm)
    
    def handle_sigterm(self, signum, frame):
        print("Recebido sinal SIGTERM. Realizando operações de encerramento...")
        # Adicione aqui qualquer código que você deseja executar antes de encerrar
        sys.exit(0)

    def run(self):
        self.app.run(port=8080, debug=True)

    @cross_origin()
    def api_inference(self):
        data = json.loads(request.data)
        response, code = self.zeroMQClient.send_message("inference", data)
        
        return jsonify(response), code
    
    @cross_origin()
    def api_review(self):
        data = json.loads(request.data)
        response, code = self.zeroMQClient.send_message("review", data)
        
        return jsonify({'response': response}), code



if __name__ == "__main__":
    api_server = APIServer()
    api_server.run()
