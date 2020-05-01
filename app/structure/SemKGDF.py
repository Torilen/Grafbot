import pandas as pd

class SemKGDF:
    graph = pd.DataFrame(columns=["s", "o", "occur"])

    def get_occur_relation(self, s, o):
        return self.graph[(self.graph.s == s) & (self.graph.o == o)].occur

    def get_graph(self):
        return self.graph

    def isRelExist(self, s, o):
        return len(self.graph[((self.graph.s == s) & (self.graph.o == o)) | ((self.graph.o == s) & (self.graph.s == o))]) > 0

    def add_relations(self, rels):

        rels_to_concat = list()
        for rel in rels:
            s = rel[0]
            o = rel[1]

            rels_in_graph = self.graph[((self.graph.s == s) & (self.graph.o == o)) | ((self.graph.o == s) & (self.graph.s == o))]

            if(len(rels_in_graph) > 1):
                for index, row in rels_in_graph:
                    self.graph.at[index, "occur"] = self.graph.at[index, "occur"] + 1
            else:
                rels_to_concat.append(s, o, 1)
                rels_to_concat.append(o, s, 1)


    def toJson(self):
        return self.graph.to_json()

