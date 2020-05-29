from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api
from flask_cors import CORS, cross_origin
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from tools.Translator import translate, detect, translate_by_url
from tools.VoiceSynthetiser import speak
from tools.Utils import process_output_chatbot
import json
import base64
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
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def post(self):
        user_language = detect(request.form['data'])
        print("Language user detected : {}".format(user_language))
        print("User base version : " + request.form['data'])
        english_version_of_user_input = translate(request.form['data'], src=user_language)
        print("User english version : "+english_version_of_user_input)
        model_response = self._interactive_running(
            SHARED.get('opt'), english_version_of_user_input
        )
        json_str = model_response

        # process text
        processed_output = ""

        if (user_language != "en"):
            json_value = json_str
            print("Bot english version : " + json_value['text'])
            json_value.force_set('text', process_output_chatbot(json_value['text'], user_language))
            json_value.force_set('text', translate(json_value['text'], dest=user_language))
            print("Bot base version : " + json_value['text'])
        else:
            json_value = json_str
            print("Bot english version : " + json_value['text'])
            json_value.force_set('text', process_output_chatbot(json_value['text'], user_language))


        # speak(processed_output, user_language, env)
        # translate_by_url(json_value['text'], dest=user_language)
        return jsonify(json_value)

@api.route('/reset')
class Reset(Resource):
    def post(self):
        SHARED['agent'].reset()
        res = dict()
        res['reset'] = 1
        return jsonify(res)

@api.route('/getVoice')
class Voice(Resource):
    def get(self):
        with open("/root/Grafbot/app/web/output.mp3", "rb") as voice:
            str = base64.b64encode(voice.read()).decode("utf-8")
        return str

if __name__ == '__main__':
    parser = setup_args()
    SHARED['opt'] = parser.parse_args(print_args=True)
    #print(SHARED['opt'])
    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])
    #print(SHARED)
    app.run(host='185.157.247.164', port='5000', debug=True)
