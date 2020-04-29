import nltk

from nltk.tag.stanford import StanfordPOSTagger
root_path="lib/stanford-postagger-full-2018-10-16/"
pos_tagger = StanfordPOSTagger(root_path + "models/french.tagger", root_path + "stanford-postagger.jar", encoding='utf8')
entity_tag = ['ADJ', 'ET', 'NC', 'NP', 'PRO', 'N']

def pos_tag(sentence):
    tokens = nltk.word_tokenize(sentence)
    tags = pos_tagger.tag(tokens)
    return tags

def get_good_words(sentence_tagged):
    i = list()
    index_word = 0
    for entity in sentence_tagged:
        if(entity[1] in entity_tag):
            i.append([entity[0], index_word])
        index_word+=1

    return i

def get_entities(sentence):
    return(get_good_words(pos_tag(sentence)))