import nltk
from nltk.tree import Tree
from nltk.corpus import sinica_treebank
 
# print(sinica_treebank.words())

print(sinica_treebank.parsed_sents()[36].draw())
# print(Tree.fromstring(sinica_treebank.parsed_sents()[33]).draw())