from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any

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

    def get(self, val):
        if val == 'opt':
            return self.opt
        elif val == 'agent':
            return self.agent
        elif val == 'world':
            return self.world
        else:
            return None