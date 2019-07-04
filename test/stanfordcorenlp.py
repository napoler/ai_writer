from nltk.tree import Tree

from stanfordcorenlp import StanfordCoreNLP
sentence = '我叫小米'
#https://stanfordnlp.github.io/CoreNLP/history.html
with StanfordCoreNLP(r'/home/terry/nltk_data/coreNLP/', lang='zh') as nlp:
    Tree.fromstring(nlp.parse(sentence)).draw()