from flask import Flask, request, send_file
from flask_restplus import Resource, Api
from flask_cors import CORS, cross_origin
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from tools.Translator import translate, detect
from tools.VoiceSynthetiser import speak
from tools.Utils import process_output_chatbot
import json
import base64

app = Flask(__name__)
CORS(app)

#api = Api(app)

SHARED: Dict[Any, Any] = {}

@app.route('/interact')
class Interact(Resource):
    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def post(self):
        user_language = detect(request.form['data'])
        print("Language user detected : {}".format(user_language))
        english_version_of_user_input = translate(request.form['data'], src=user_language)
        print(english_version_of_user_input)
        model_response = self._interactive_running(
            SHARED.get('opt'), english_version_of_user_input
        )
        json_str = model_response
        if (user_language != "en"):
            json_value = json.loads(json_str)
            print(json_value['text'])
            json_value['text'] = translate(json_value['text'], dest=user_language)
        else:
            json_value = json_str

        # process text
        processed_output = process_output_chatbot(json_value['text'], user_language)
        speak(processed_output, user_language)
        json_value.force_set('text', processed_output)
        return json_value

@app.route('/reset')
class Reset(Resource):
    def post(self):
        SHARED['agent'].reset()

@app.route('/getVoice')
class Voice(Resource):
    def get(self):
        return send_file("web/output.mp3", as_attachment=True)

if __name__ == '__main__':
    parser = setup_args()
    SHARED['opt'] = parser.parse_args(print_args=False)
    print(SHARED['opt'])

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])
    app.run(host='185.157.246.81',port='5000', debug=True)
