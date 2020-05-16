import cppyy
import os
import random

cppyy.add_include_path(str(os.getcwd()) + "/sleepygraph/")
cppyy.include("VectorNode.h")
cppyy.include("VectorEdge.h")
cppyy.include("UndirectedGraph.h")

from cppyy.gbl import UndirectedGraph, VectorNode, VectorEdge

nodes = VectorNode()
for i in range(0, 5):
    nodes.append(i, "Sommet"+str(i))

edges = VectorEdge()
for i in range(0, 5):
    edges.append(nodes[i], nodes[(i+1)%5], random.randint(1,10), random.randint(10,20))

graph = UndirectedGraph(nodes, edges)

print(graph.toString())
