import re
import uuid
import sqlite3
import datetime
import tensorflow as tf
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "TransformerChatbot")
sys.path.append(parent_dir)

from ZmqServer import ZmqServer, Message
from TransformerChatbot.Layers import TextIDMapper
from TransformerChatbot.Models import Chatbot
from TransformerChatbot.Utils import download_trained_weights


class DBConnection:
    def __init__(self):
        self._conn = self._get_connection()

    @staticmethod
    def _get_connection():
        conn = sqlite3.connect("./conversations.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Conversation(id UUID PRIMARY KEY, sentence TEXT,
            actor VARCHAR(20), feedback INTEGER, created_at DATETIME);
        """)
        conn.commit()
        return conn

    def execute(self, query: str):
        cur = self._conn.cursor()
        self._conn.execute("BEGIN TRANSACTION;")
        try:
            cur.execute(query)
            self._conn.commit()
        except Exception as ex:
            self._conn.rollback()
            raise ex


class ChatbotServer(ZmqServer):
    def __init__(self, port):
        super().__init__(port)

        self.chatbot = None
        self.conn = DBConnection()

    def build(self):
        model_path = os.path.join(current_dir, "TransformerChatbot")
        weights_path = download_trained_weights(os.path.join(model_path, "logs"))
        text_processor = TextIDMapper()
        text_processor.load_vocab(os.path.join(model_path, 'Data/tokens_by_type.json'))

        self.chatbot = Chatbot(text_processor)
        self.chatbot(tf.convert_to_tensor((['olá'], ['olá'])))
        self.chatbot.load_weights(weights_path)
        self.logger.info("Chatbot is ready")

    def _handle_request(self, message: Message):
        self.logger.info("REQ TYPE: {} | data: {}".format(
            message.req_type,
            message.data,
        ))

        if message.req_type == "inference":
            return self._process_inference(message.data)
        elif message.req_type == "review":
            return self._process_review(message.data)

    def _process_review(self, data):
        self.conn.execute(
            """UPDATE Conversation SET feedback={} WHERE id='{}';""".format(
                int(data["feedback"]), data["id"]
            )
        )
        
        return {"status": True}

    def _process_inference(self, data):
        response_text, _, _ = self.chatbot.predict(data["sentence"])
        response_text = response_text.numpy().decode('utf-8')
        response_id = str(uuid.uuid4())
        self.logger.info("Text response generated by chatbot: '{}'".format(response_text))

        self.conn.execute("""
            INSERT INTO Conversation (id, sentence, actor, created_at)
            VALUES('{}', '{}', '{}', '{}');""".format(
                data["id"], data["sentence"], "User", datetime.datetime.now()
            )
        )
        self.conn.execute("""
            INSERT INTO Conversation (id, sentence, actor, created_at)
            VALUES('{}', '{}', '{}', '{}');""".format(
                response_id, response_text, "Bot", datetime.datetime.now()
            )
        )

        response_text = response_text if response_text != '. . .' else 'não sei'
        examples = re.findall(r"`.*?`", response_text)
        languages = re.findall(r"<lang.*?>", response_text)
        for i in range(len(examples)):
            response_text = response_text.replace(examples[i], "")
            examples[i] = examples[i].replace(languages[i], "")
            examples[i] = examples[i].replace("`", "").strip().replace("<br>", "\n")
            languages[i] = languages[i].replace("<lang", "").replace(">", "").capitalize()

        return {
            "id": response_id,
            "actor": "Bot",
            "text": response_text,
            "examples": examples,
            "languages": languages,
        }


if __name__ == "__main__":
    server = ChatbotServer(5555)
    server.start()
