import json

class SemKG:
    graph = dict()
    graphNodeId = dict()

    def get_occur_relation(self, s, o):
        return self.graph[(s, o)]

    def get_graph(self):
        return {"graph": self.graph, "nodesId": self.graphNodeId}

    def to_json(self):
        return json.dumps(self.get_graph())

    def load_from_json(self, json):
        data = json.loads(json)
        self.graph = data["graph"]
        self.graphNodeId = data["nodesId"]

    def save(self, path, name="semkg.json"):
        with open(path+"/"+name, 'w') as json_file:
            json.dump(self.to_json(), json_file)

    def add_node(self, node):
        if node not in list(self.graphNodeId.keys()):
            self.graphNodeId[node] = len(list(self.graphNodeId.keys()))+1

    def get_node_id(self, node):
        return self.graphNodeId[node]

    def add_relation(self, s, o):
        self.add_node(s)
        self.add_node(o)

        if (s, o) not in list(self.graph.keys()):
            if (o, s) not in list(self.graph.keys()):
                self.graph[(s, o)] = 1
                self.graph[(o, s)] = 1
            else:
                self.graph[(o, s)] += 1
                self.graph[(s, o)] = self.graph[(s, o)]
        else:
            self.graph[(s, o)] += 1
            self.graph[(o, s)] = self.graph[(s, o)]

    def add_relations(self, rels, epikg, input):
        for rel in rels:
            s = rel[0]
            o = rel[1]
            print("Tuples")
            print(rel)
            self.add_relation(s[0], o[0])
            epikg.add_relation(self.graphNodeId[s[0]], self.graphNodeId[o[0]], input, s[1], o[1])

    def get_stories(self, epikg, entities, top_n=5, steps=5):
        stories = epikg.get_stories([self.graphNodeId[e] for e in entities], top_n, steps)
        return 0