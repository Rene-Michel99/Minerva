import os
import zmq
import json
import logging


class ZeroMQClient:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.RCVTIMEO = 50000
        self.socket.connect("tcp://localhost:5555")
        
        self.logger = logging.getLogger('MaskRCNN')
        self.logger.setLevel(logging.DEBUG)

        level = logging.DEBUG
        if not os.path.exists('./logs'):
            os.system("mkdir logs")
        path_to_log = './logs/zmq_client.log'
        handler = logging.FileHandler(filename=path_to_log, encoding='utf-8')

        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(logging.StreamHandler())

    def send_message(self, req_type: str, data: dict):
        try:
            message = self._build_request(req_type, data)
            self.logger.info("Sending request to ZMQ server: {}".format(message))
            
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv().decode('utf-8')
            
            self.logger.info("Response received from server: {}".format(response))
            
            return json.loads(response), 200
        except Exception as ex:
            print(ex)
            return str(ex), 500
    
    def _build_request(self, req_type: str, data: dict):
        return "{}\t{}".format(req_type, json.dumps(data))

