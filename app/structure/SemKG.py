import json
import numpy as np

class SemKG:
    graph = dict()
    graphNodeId = dict()
    graphNeighbour = dict()

    def get_occur_relation(self, s, o):
        return self.graph[(s, o)]

    def get_graph(self):
        return {"graph": self.graph, "nodesId": self.graphNodeId, "successor": self.graphSuccessor}

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
        if node in list(self.graphNodeId.keys()):
            return self.graphNodeId[node]
        else:
            return -1

    def add_relation(self, s, o):
        self.add_node(s)
        self.add_node(o)

        if (s, o) not in list(self.graph.keys()):
            if (o, s) not in list(self.graph.keys()):
                self.graph[(s, o)] = 1
                self.graph[(o, s)] = 1
            else:
                self.graph[(o, s)] += 1
                self.graph[(s, o)] = self.graph[(o, s)]
        else:
            self.graph[(s, o)] += 1
            self.graph[(o, s)] = self.graph[(s, o)]

        if s in list(self.graphNeighbour.keys()):
            if o not in self.graphNeighbour[s]:
                self.graphNeighbour[s].append(o)
        else:
            self.graphNeighbour[s] = list()
            self.graphNeighbour[s].append(o)

        if o in list(self.graphNeighbour.keys()):
            if s not in self.graphNeighbour[o]:
                self.graphNeighbour[o].append(s)
        else:
            self.graphNeighbour[o] = list()
            self.graphNeighbour[o].append(s)


    def add_relations(self, rels, epikg, input):
        for rel in rels:
            s = rel[0]
            o = rel[1]
            print("Tuples")
            print(rel)
            self.add_relation(s[0], o[0])
            epikg.add_relation(self.graphNodeId[s[0]], self.graphNodeId[o[0]], input, s[1], o[1])

    def get_all_nodes_in_neighbour(self, entity):
        #print(list(self.graphNeighbour.keys()))
        if(entity in list(self.graphNeighbour.keys())):
            neighbour = self.graphNeighbour[entity]
            weights = [self.graph[(entity, n)] for n in neighbour]
            res = []

            for j in range(min(3, len(weights))):
                index_max = np.argmax(weights)
                res.append([neighbour[index_max], weights[index_max]])
                weights[index_max] = 0
        else:
            res = []

        return res

    def semantic_propagation(self, entity, steps, i):
        childs = self.get_all_nodes_in_neighbour(entity)
        print("CHILDS: ["+', '.join(childs)+"]")
        l = list(entity)
        for child in childs:
            # child[0] => entity | #child[1] => weight
            l.append(child[0])
            print(child[0])
        print("L: "+l)
        for child in childs:
            if(i < steps):
                res_t = self.semantic_propagation(child[0], steps, i+1)
                #print(res_t)
                l = [*l, *self.semantic_propagation(child[0], steps, i+1)]
            else:
                return l
        return l

    def get_stories(self, epikg, entities, top_n=5, steps=5):
        graph_nodes_neighbours = list()
        for e in entities:
            propa = self.semantic_propagation(e, steps, 0)
            for s in propa:
                if(s not in graph_nodes_neighbours):
                    graph_nodes_neighbours.append(s)
        print(entities, graph_nodes_neighbours)
        stories = epikg.get_stories([self.graphNodeId[e] for e in entities+graph_nodes_neighbours], top_n, steps)
        return stories