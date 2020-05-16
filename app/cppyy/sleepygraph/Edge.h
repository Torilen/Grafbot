#include "Node.h"
#include <string>
#include <iostream>

#ifndef EDGE_H
#define EDGE_H

class Edge
{
private:
    Node *source;
    Node *target;
    double weight;
    double capacity;

public:
    Edge()
    {
        this->source = NULL;
        this->target = NULL;
        this->weight = 0;
        this->capacity = 0;
    }
    Edge(Node *source, Node *target, double weight = 0, double capacity = 0)
    {
        this->source = source;
        this->target = target;
        this->weight = weight;
        this->capacity = capacity;
    }
    ~Edge(){}

    // accessors
    Node *getSource() { return this->source; }
    void setSource(Node *source) { this->source = source; }
    Node *getTarget() { return this->target; }
    void setTarget(Node *target) { this->target = target; }
    double getWeight() { return this->weight; }
    void setWeight(double weight) { this->weight = weight; }
    double getCapacity() { return this->capacity; }
    void setCapacity(double capacity) { this->capacity = capacity; }

    std::string toString(bool undirected, std::string space = ""){
        std::string arrow = undirected ?  " ===> " : " <==> " ;
        return std::to_string((*this->source).getIndex()) + arrow + std::to_string((*this->target).getIndex()) + " = (Weight,Capacity) : ("
            + std::to_string(this->weight) + "," + std::to_string(this->capacity) + ")\n";
    }
};

#endif