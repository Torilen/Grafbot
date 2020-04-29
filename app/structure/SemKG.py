class SemKG:
    graph = dict()
    graphNodeId = dict()

    def get_occur_relation(self, s, o):
        return self.graph[(s, o)]

    def get_graph(self):
        return {"graph": self.graph, "nodesId": self.graphNodeId}

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

    def add_relations(self, rels):
        for rel in rels:
            s = rel[0]
            o = rel[1]

            self.add_relation(s, o)

    def get_stories(self, epikg, entities, top_n=5):
        return 0