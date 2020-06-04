from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from flask_cors import CORS
from typing import Dict, Any

from tools.Utils import process_output_chatbot
from structure.GrafbotAgent import GrafbotAgent

env = "ubuntu"
app = Flask(__name__)
api = Api(app)
CORS(app)

#api = Api(app)

SHARED: Dict[Any, Any] = {}

@api.route('/interact')
class Interact(Resource):
    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED[request.remote_addr].get('agent').observe(reply)
        model_res = SHARED[request.remote_addr].get('agent').act()
        return model_res

    def post(self):
        if(not request.remote_addr in list(SHARED.keys())):
            SHARED[request.remote_addr] = GrafbotAgent(personality = ["My name is Bettana",
                                                        "I\'m 25 years old",
                                                        "I\'m a fashion advisor",
                                                        "I\'m vegan",
                                                        "My cat can kill a dog"])
        return SHARED[request.remote_addr].speak(request.form['data'])

@api.route('/reset')
class Reset(Resource):
    def post(self):
        SHARED[request.remote_addr].get('agent').reset()
        res = dict()
        res['reset'] = 1
        return jsonify(res)

if __name__ == '__main__':
    app.run(host='185.157.247.164', debug=True)
