import json
import os
import sys
import zmq
import logging
import signal
from abc import ABC, abstractmethod


class Message:
    def __init__(self, req_type: str, data: dict):
        self.req_type = req_type
        self.data = data


class ZmqServer(ABC):
    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(self.port))

        self.logger = logging.getLogger('MaskRCNN')
        self.logger.setLevel(logging.DEBUG)

        level = logging.DEBUG
        if not os.path.exists('./logs'):
            os.system("mkdir logs")
        path_to_log = './logs/zmq_server.log'
        handler = logging.FileHandler(filename=path_to_log, encoding='utf-8')

        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info("ZMQ Server is ready!")
        signal.signal(signal.SIGTERM, self.handle_sigterm)
    
    def handle_sigterm(self, signum, frame):
        print("Recebido sinal SIGTERM. Realizando operações de encerramento...")
        # Adicione aqui qualquer código que você deseja executar antes de encerrar
        sys.exit(0)

    @abstractmethod
    def build(self):
        raise NotImplementedError()

    def start(self):
        self.build()
        self.logger.info("ZMQ Server started!")
        while True:
            #  Wait for next request from client
            message = self._receive_message()
            if message.req_type == "shutdown":
                break

            try:
                response = self._handle_request(message)
                response = self._pack_response(response)
                self.logger.info("Response: {}".format(response))
            except Exception as ex:
                self.logger.exception(ex)
                response = self._pack_response({"error": str(ex)})

            #  Send reply back to client
            self.socket.send(response.encode('utf-8'))

    @staticmethod
    def _pack_response(response: dict):
        return json.dumps(response)

    def _receive_message(self) -> Message:
        message = self.socket.recv().decode('utf-8')
        self.logger.info("Message received: {}".format(message))
        message_data = message.split('\t')[1].replace("b'", "").replace("'", "")

        return Message(
            req_type=message.split('\t')[0],
            data=json.loads(message_data)
        )

    @abstractmethod
    def _handle_request(self, message):
        raise NotImplementedError()

