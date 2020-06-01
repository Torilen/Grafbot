from flask import Flask, request, send_file, jsonify
from flask_restplus import Resource, Api
from flask_cors import CORS, cross_origin
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from tools.Translator import translate_base, detect, translate_by_url, translate_by_api
from tools.VoiceSynthetiser import speak
from tools.Utils import process_output_chatbot
import ssl
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('certificate.crt', 'privateKey.key')
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
        print(SHARED['agent'])
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def post(self):
        user_language = detect(request.form['data'])
        print("Language user detected : {}".format(user_language))
        print("User base version : " + request.form['data'])
        english_version_of_user_input = translate_base(request.form['data'], src=user_language)
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
            json_value.force_set('text', translate_by_api(json_value['text'], env, dest=user_language))
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
    SHARED['opt'] = parser.parse_args(print_args=False)

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    print("Init agent : {}".format(agent))
    agent.observe({'episode_done': False, 'text': 'your persona: My name is Bettana \nyour persona: I\'m 25 years old \nyour persona: I\'m a fashion advisor \nyour persona: Your name is Aniss \nyour persona: I\'m vegan \nyour persona: My cat can kill a dog'})
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])
    print(SHARED)
    app.run(host='185.157.247.164', debug=True)
