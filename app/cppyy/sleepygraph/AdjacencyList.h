#include "Edge.h"
#include "Node.h"
#include "VectorNode.h"
#include "VectorEdge.h"
#include <vector>
#include <string>
#include <iostream>

#ifndef ADJACENCYLIST_H
#define ADJACENCYLIST_H

class AdjacencyList
{
private:
    VectorNode nodes;
    std::vector<VectorEdge> edges;

public:
    AdjacencyList(int nodeNumber)
    {
        for (int i = 0; i < nodeNumber; i++)
        {
            this->edges.push_back(VectorEdge());
            nodes.push_back(new Node(i, ""));
        }
    }
    AdjacencyList(VectorNode node)
    {
        this->nodes = node;
        for (int i = 0; i < node.size(); i++)
        {
            this->edges.push_back(VectorEdge());
        }
    }
    AdjacencyList(VectorNode node, VectorEdge edge)
    {
        this->nodes = node;
        for (int i = 0; i < node.size(); i++)
        {
            this->edges.push_back(VectorEdge());
        }
        for (std::vector<Edge *>::iterator i = edge.vector.begin(); i != edge.vector.end(); ++i)
        {
            this->edges[(*(**i).getSource()).getIndex()].push_back((*i));
        }
    }
    ~AdjacencyList() {}

    // methods

    /*
        Add a node to the adjacency list, returning if it suceed or not
    */
    bool AddNode(std::string name = "")
    {
        try
        {
            this->nodes.push_back(new Node(this->nodes.size(), name));
            this->edges.push_back(VectorEdge());
            return true;
        }
        catch (...)
        {
            std::cout << "Error while adding a Node" << std::endl;
            return false;
        }
    }

    /*
        Add an vertice, returning if it suceed or not
    */
    bool AddEdge(Edge e, bool reverse)
    {
        try
        {
            if ((*e.getTarget()).getIndex() < this->nodes.size())
            {
                Edge *edge = new Edge();
                (*edge) = e;
                this->edges[(*e.getSource()).getIndex()].push_back(edge);
                if (reverse)
                {
                    Edge *edgeReversed = new Edge(e.getTarget(), e.getSource(), e.getWeight(), e.getCapacity());
                    this->edges[(*e.getSource()).getIndex()].push_back(edgeReversed);
                }
                return true;
            }
            return false;
        }
        catch (...)
        {
            std::cout << "Error while adding an Edge" << std::endl;
            return false;
        }
    }

    /*
        Check whether or not an edges between source and target provided
    */
    bool HasTarget(int source, int target)
    {
        if (source < this->edges.size())
        {
            VectorEdge neightbors = this->edges[source];
            for (std::vector<Edge *>::iterator i = neightbors.vector.begin(); i != neightbors.vector.end(); ++i)
            {
                if ((*(*(*i)).getTarget()).getIndex() == target)
                {
                    return true;
                }
            }
            return false;
        }
        return false;
    }

    /*
        Print Adjacency List
    */
    std::string toString(bool undirected)
    {
        std::string printed = "---------------------- # ----------------------\n";
        printed += "--------------- Printing Graph ----------------\n";
        printed += "---------------------- - ----------------------\n";
        printed += "--> Nodes :\n";
        for (std::vector<Node *>::iterator i = this->nodes.begin(); i != this->nodes.end(); ++i)
        {
            printed += (**i).toString("   ");
        }
        printed += "\n--> Edges :\n";
        for (std::vector<VectorEdge>::iterator i = this->edges.begin(); i != this->edges.end(); ++i)
        {
            for (std::vector<Edge *>::iterator j = (*i).vector.begin(); j != (*i).vector.end(); ++j)
            {
                printed += (**j).toString(undirected, "   ");
            }
        }
        printed += "---------------------- - ----------------------\n";
        printed += "--------------- Printing Graph ----------------\n";
        printed += "---------------------- # ----------------------\n";
        return printed;
    }
};

#endif