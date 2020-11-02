import time
import pandas as pd
import numpy as np
import json

class EpiKG:
    graph_a_pointed_b = dict()
    graph_a_pointed_b_direct = dict()

    sem_to_stories_with_context = dict()

    def get_graph(self):
        return {"predicate_root": self.graph_a_pointed_b, "s_root": self.graph_a_pointed_b_direct}

    def to_json(self):
        return json.dumps(self.get_graph())

    def load_from_json(self, json):
        data = json.loads(json)
        self.graph_a_pointed_b = data["predicate_root"]
        self.graph_a_pointed_b_direct = data["s_root"]

    def save(self, path, name="epikg.json"):
        with open(path+"/"+name, 'w') as json_file:
            json.dump(self.to_json(), json_file)

    def add_relation(self, s, o, input, index1, index2):
        #print(index1, index2)
        p = self.predict_relation(s, o, input, index1, index2)
        t = time.time()
        print(str(t))
        if(p not in list(self.graph_a_pointed_b.keys())):
            self.graph_a_pointed_b[p] = dict()
            self.graph_a_pointed_b[p][s] = dict()
            self.graph_a_pointed_b[p][s][o] = [t, input]
        else:
            if(s not in list(self.graph_a_pointed_b[p].keys())):
                self.graph_a_pointed_b[p][s] = dict()
                self.graph_a_pointed_b[p][s][o] = [t, input]
            else:
                if(o not in self.graph_a_pointed_b[p][s].keys()):
                    self.graph_a_pointed_b[p][s][o] = [t, input]

        if(s not in list(self.graph_a_pointed_b_direct.keys())):
            self.graph_a_pointed_b_direct[s] = dict()
            if(o not in list(self.graph_a_pointed_b_direct[s].keys())):
                self.graph_a_pointed_b_direct[s][o] = [p]
            else:
                if (p not in self.graph_a_pointed_b_direct[s][o]):
                    self.graph_a_pointed_b_direct[s][o].append(p)
        else:
            if (o not in list(self.graph_a_pointed_b_direct[s].keys())):
                self.graph_a_pointed_b_direct[s][o] = [p]
            else:
                if (p not in self.graph_a_pointed_b_direct[s][o]):
                    self.graph_a_pointed_b_direct[s][o].append(p)


    def predict_relation(self, s, o, input, index1, index2):
        rel = input.lower().split()[index1+1:index2]
        print(rel)
        if(len(rel) > 0):
            return " ".join(rel)
        else:
            return ""

    def add_relations(self, rels, input):
        for rel in rels:
            s = rel[0][0]
            o = rel[1][0]
            p = self.predict_relation(s, o, input, str(rel[0][1]), str(rel[1][1]))

            self.add_relation(s, o, p)

    def get_all_node_ids_pointed_by_s(self, s):
        node_ids = list()
        if s in list(self.graph_a_pointed_b_direct.keys()):
            for key in self.graph_a_pointed_b_direct[s].keys():
                for p in self.graph_a_pointed_b_direct[s][key]:
                    node_ids.append([key, p])
        return node_ids

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def classify_stories_zone(self, stories):
        delay = []
        for i in range(len(stories)-1):
            delay.append(stories.loc[i+1].time - stories.loc[i].time)
        print(delay)
        index_limit_stories = []
        if(len(delay) > 0):
            prob_delay = self.softmax(delay)
            mean_prob_delay = np.mean(prob_delay)

            for i in range(len(prob_delay)):
                if (prob_delay[i] > mean_prob_delay):
                    index_limit_stories.append(i)
        return index_limit_stories

    def get_stories(self, entities, top_n, steps):
        graph_content_stories = list()
        for e in entities:
            st = self.episodic_propagation(e, steps, 0)
            for s in st:
                if(s not in graph_content_stories):
                    graph_content_stories.append(s)


        stories_sample = pd.DataFrame(graph_content_stories, columns=["s", "o", "p", "time", "sentence", "distance"]).sort_values(by=['time'])
        #stories_sample['sentence'] = stories_sample[['s', 'p', '0']].agg(' '.join, axis=1)
        print(stories_sample)
        stories = []
        index_limit_stories = self.classify_stories_zone(stories_sample)
        ind = 0
        ind_sup = 0
        for ind_sup in index_limit_stories:
            stories.append(stories_sample.iloc[ind:ind_sup])
            ind = ind_sup
        stories.append(stories_sample.iloc[ind_sup:len(stories_sample)])

        return stories


    def episodic_propagation(self, entity, steps, i):
        childs = self.get_all_node_ids_pointed_by_s(entity)
        l = list()
        for child in childs:
            l.append([entity, child[0], child[1], self.graph_a_pointed_b[child[1]][entity][child[0]][0], self.graph_a_pointed_b[child[1]][entity][child[0]][1], len(child[1].split())])
        for child in childs:
            if(i < steps):
                l = l+self.episodic_propagation(child[0], steps, i+1)
            else:
                return l
        return l
