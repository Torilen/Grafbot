#include "Node.h"
#include <vector>

#ifndef VECTORNODE_H
#define VECTORNODE_H

class VectorNode{
    public:
        std::vector<Node*> vector;

    void append(Node n) 
    { 
        Node *node = new Node();
        (*node) = n;
        this->vector.push_back(node);
    } 
    void append(int index = 0, std::string name = "") 
    { 
        Node *node = new Node(index, name);
        this->vector.push_back(node);
    } 

    size_t size(){
        return this->vector.size();
    }

    Node* operator[](int index) 
    { 
        return this->vector[index];
    } 

    std::vector<Node*>::iterator begin(){
        return this->vector.begin();
    }

    std::vector<Node*>::iterator end(){
        return this->vector.end();
    }

    void push_back(Node *n){
        this->vector.push_back(n);
    }


};

#endif