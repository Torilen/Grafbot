from flask import jsonify
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from tools.Translator import translate_base, detect, translate_by_url, translate_by_api
from tools.Utils import process_output_chatbot

class GrafbotAgent:
    parser = setup_args()
    opt = None
    agent = None
    world = None

    def __init__(self, personality):
        self.opt = self.parser.parse_args(print_args=False)
        self.opt['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'
        self.agent = create_agent(self.opt, requireModelExists=True)
        personalityText = ' \n'.join(["your persona: "+personaField for personaField in personality])
        self.agent.observe({'episode_done': False, 'text': personalityText})
        self.world = create_task(self.opt, self.agent)

    def speak(self, reply_text, res):
        user_language = detect(reply_text)

        english_version_of_user_input = translate_base(reply_text, src=user_language)

        reply = {'episode_done': False, 'text': english_version_of_user_input}
        self.get('agent').observe(reply)
        model_res = self.get('agent').act()

        json_return = dict()

        if (user_language != "en"):
            json_return['text'] = process_output_chatbot(model_res['text'], user_language)
            json_return['text'] = translate_by_api(json_return['text'], "ubuntu", dest=user_language)
        else:
            json_return['text'] = process_output_chatbot(model_res['text'], user_language)

        json_return['user_lang'] = user_language
        res = jsonify(json_return)

    def get(self, val):
        if val == 'opt':
            return self.opt
        elif val == 'agent':
            return self.agent
        elif val == 'world':
            return self.world
        else:
            return None