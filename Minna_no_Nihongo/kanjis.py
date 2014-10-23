#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from glob import glob

import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json

import itertools
import unicodedata as ud


def get_words_from_files(files):
    h = re.compile(r"(.*?)\[(.*?)\] (.*)")
    words = {}
    for fn in files:
        #print fn
        chapter = int(fn.split(".")[1])
        with open(fn) as file:
            # skip intro
            for i in range(4): line = file.readline()
            while line:
                line = file.readline()
                # end of line
                if line.startswith("#end"): break
                m = h.match(line)
                word, kana, meaning = m.group(1).decode('utf-8'), m.group(2).decode('utf-8'), m.group(3)
                words[word] = {"chapter":chapter,"kana":kana, "meaning":meaning}

    return words


def main():
    files = []
    for i in range(1,26): files.append("db/Minna_no_nihongo_1.%02d.txt" % i)
    for i in range(26,51): files.append("db/Minna_no_nihongo_2.%02d.txt" % i)


    data = get_words_from_files(files)
    words = [w for w in data]
    #print words
    G=nx.Graph()
    for word1, word2 in itertools.combinations(words,2):
        for w1 in word1[:-1]:
            #print w1.encode('utf-8')
            #print ud.name(w1)
            if "CJK UNIFIED" in ud.name(w1) and w1 in word2:
                #print word1.encode('utf-8'), word2.encode('utf-8')
                G.add_edge(word1, word2)
                break
    
    nx.draw(G)
    nx.write_dot(G, "kanjis.dot")
    nx.write_graphml(G, "kanjis.graphml")
    #plt.show()

    words = G.nodes()

    with open('kanjis.json', 'w') as f:
        json.dump({'nodes': [{'name': i.encode('utf-8'), 
                              'kana': data[i]['kana'], 
                              'chapter': data[i]['chapter'],
                              'meaning': data[i]['meaning']} for i in G.nodes()], 
                   'links': list(map(lambda u: {'source': words.index(u[0]), 'target': words.index(u[1])}, G.edges()))}, 
              f, indent=2,)


if __name__ == "__main__":
    main()
