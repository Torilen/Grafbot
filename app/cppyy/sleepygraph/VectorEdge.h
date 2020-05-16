#include "Edge.h"
#include <vector>

#ifndef VECTOREDGE_H
#define VECTOREDGE_H

class VectorEdge
{
public:
    std::vector<Edge*> vector;

    void append(Edge e) 
    { 
        Edge *edge = new Edge();
        (*edge) = e;
        this->vector.push_back(edge);
    } 
    void append(Node *source, Node *target, double weight = 0, double capacity = 0) 
    { 
        Edge *edge = new Edge(source, target, weight, capacity);
        this->vector.push_back(edge);
    } 

    VectorEdge reverse(){
        VectorEdge reversed;
        for(std::vector<Edge*>::iterator i = this->vector.begin(); i != this->vector.end(); ++i){
            reversed.push_back(new Edge((**i).getTarget(), (**i).getSource(), (**i).getWeight(), (**i).getCapacity()));
        }
        return reversed;
    }

    size_t size(){
        return this->vector.size();
    }

    Edge* operator[](int index) 
    { 
        return this->vector[index];
    } 

    std::vector<Edge *>::iterator begin()
    {
        return this->vector.begin();
    }

    std::vector<Edge *>::iterator end()
    {
        return this->vector.end();
    }

    void push_back(Edge *n)
    {
        this->vector.push_back(n);
    }
};

#endif