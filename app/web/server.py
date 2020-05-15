from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
from tools.Translator import translate, detect
from tools.VoiceSynthetiser import speak
from tools.Utils import process_output_chatbot
import json
import base64

user_language = "fr"
HOST_NAME = 'localhost'
PORT = 8080

SHARED: Dict[Any, Any] = {}


class MyHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        model_res = SHARED['agent'].act()
        return model_res

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            user_language = detect(body.decode('utf-8'))
            print("Language user detected : {}".format(user_language))
            english_version_of_user_input = translate(body.decode('utf-8'), src=user_language)
            print(english_version_of_user_input)
            model_response = self._interactive_running(
                SHARED.get('opt'), english_version_of_user_input
            )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            #model_response.text = translate(model_response.text, dest=user_language)

            json_str = json.dumps(model_response)
            if(user_language != "en"):
                json_value = json.loads(json_str)
                print(json_value['text'])
                json_value['text'] = translate(json_value['text'], dest=user_language)
                json_str = json.dumps(json_value)

            #process text
            json_value = json.loads(json_str)

            json_value['text'] = process_output_chatbot(json_value['text'], user_language)
            json_str = json.dumps(json_value)
            answer_bot = bytes(json_str, 'utf-8')
            print(answer_bot)
            self.wfile.write(answer_bot)
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            SHARED['agent'].reset()
            self.wfile.write(bytes("{}", 'utf-8'))
        elif self.path == '/getVoice':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            self.send_response(200)
            self.send_header('Content-type', 'audio/mpeg;base64')
            self.end_headers()

            speak(body.decode('utf-8'), detect(body.decode('utf-8')))
            with open("web/output.mp3", mode='rb') as voice:
                voice_encoded = base64.b64encode(voice.read())
            self.wfile.write(voice_encoded)
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = ""
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def setup_interactive(shared):
    """
    Build and parse CLI opts.
    """
    parser = setup_args()
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on.')
    parser.add_argument(
        '--host',
        default=HOST_NAME,
        type=str,
        help='Host from which allow requests, use 0.0.0.0 to allow all IPs',
    )

    SHARED['opt'] = parser.parse_args(print_args=False)

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    # show args after loading model
    parser.opt = agent.opt
    parser.print_args()
    return agent.opt