#include <string>
#include <iostream>
#include <vector>

#ifndef NODE_H
#define NODE_H

class Node
{
private:
    int index;
    std::string name;

public:
    Node(int index = 0, std::string name = "")
    {
        this->index = index;
        this->name = name;
    };
    ~Node(){};

    // accessors
    int getIndex(){ return this->index; }
    void setIndex(int index=0){ this->index = index; }
    std::string getName() { return this->name; };
    void setName(std::string name = "") { this->name = name; }

    std::string toString(std::string space = ""){
        return space + std::to_string(this->index) + " <-> " + this->name + "\n";
    }
};

#endif