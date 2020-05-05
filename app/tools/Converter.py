def Entities2Tuples(entities, mode="linear"):
    tuples = list()
    if(mode=="linear"):
        for i in range(len(entities)-1):
            tuples.append([entities[i], entities[i+1]])
    elif(mode=="quadratic"):
        for i in range(len(entities)):
            for j in range(len(entities)):
                if(i < j):
                    tuples.append([entities[i], entities[j]])
    return tuples
