#include "AdjacencyList.h"
#include <vector>
#include <string>
#include <iostream>

#ifndef UNDIRECTEDGRAPH_H
#define UNDIRECTEDGRAPH_H

class UndirectedGraph
{
private:
    AdjacencyList *successors = NULL;
    AdjacencyList *predecessors = NULL;

public:
    UndirectedGraph(int nodeNumber)
    {
        this->successors = new AdjacencyList(nodeNumber);
        this->predecessors = new AdjacencyList(nodeNumber);
    }
    UndirectedGraph(VectorNode node)
    {
        this->successors = new AdjacencyList(node);
        this->predecessors = new AdjacencyList(node);
    }
    UndirectedGraph(VectorNode node, VectorEdge edge)
    {
        this->successors = new AdjacencyList(node, edge);
        this->predecessors = new AdjacencyList(node, edge.reverse());
    }

    // methods

    /*
        Add a node to the adjacency list, returning if it suceed or not
    */
    bool AddNode(std::string name = "")
    {
        return this->successors->AddNode(name);
    }

    /*
        Add an vertice, returning if it suceed or not
    */
    bool AddEdge(Edge e)
    {
        return this->successors->AddEdge(e, true);
    }

    /*
        Print Adjacency List
    */
    std::string toString()
    {
        return this->successors->toString(true);
    }

    
};

#endif