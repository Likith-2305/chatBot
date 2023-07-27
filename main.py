from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from bot import chatbot
import threading
import reIndex
import os
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Chatbot API', description='API for interacting with the chatbot')

chat_ns = api.namespace('chat', description='Chatbot operations')
train_ns = api.namespace('train', description='Training operations')

chatbot_request_model = api.model('ChatbotRequest', {
    'session_id': fields.String(required=True, description='Session ID'),
    'question': fields.String(required=True, description='Question to ask the chatbot')
})

chatbot_response_model = api.model('ChatbotResponse', {
    'Answer': fields.String(description='Chatbot response')
})

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


documentPath = "./docs"

if not os.path.exists(documentPath):
    os.mkdir(documentPath)

@chat_ns.route('/')
class chat(Resource):
    @chat_ns.expect(chatbot_request_model)
    @chat_ns.response(200, 'Success', chatbot_response_model)
    def post(self):
        data = request.get_json()
        session_id = data['session_id']
        question = data['question']
        answer = None
            
        with database.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE sessionID = %s", (session_id,))
            count = cursor.fetchone()[0]
                
            if count == 0:
                question = "user: " + question + "\n"
            else:
                cursor.execute("SELECT conv FROM conversations WHERE sessionID = %s", (session_id,))
                previous_conv = cursor.fetchone()[0]
                question = previous_conv + "user: " + question + "\n"
                
            answer = chatbot(question)
            print(answer)
            if answer:
                answer = answer.lstrip("\n ")
                prefixes = ["bot: ", "Bot: "]

            for prefix in prefixes:
                if answer.startswith(prefix):
                    answer = answer[5:]

                    
            if count == 0:
                cursor.execute("INSERT INTO conversations (sessionID, conv) VALUES (%s, %s)", (session_id, question + answer+"\n"))
            else:
                cursor.execute("UPDATE conversations SET conv = %s WHERE sessionID = %s", (question + answer+"\n", session_id))
                    
            database.conn.commit()
                
           
            return answer

@train_ns.route('/')
class train(Resource):
    @train_ns.expect(upload_parser)
    @train_ns.doc('train_post')
    @train_ns.response(200, 'Success')
    def post(self):
        if request.method == "POST":
            f = request.files['file']
            f.save(documentPath+'/'+f.filename)
            thread = threading.Thread(target=reIndex.construct_index(f.filename))
            thread.start()
            return "Document added to index"
    
api.add_resource(chat, "/ask")
api.add_resource(train, "/train")

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")

