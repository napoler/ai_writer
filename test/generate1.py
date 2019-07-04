from nltk import CFG
import nltk

from recursive_descent_parser_model import RecursiveDescentParser

# # --------------------- 
# # 作者：zhuzuwei 
# # 来源：CSDN 
# # 原文：https://blog.csdn.net/zhuzuwei/article/details/79040102 
# # 版权声明：本文为博主原创文章，转载请附上博文链接！
# groucho_grammar = CFG.fromstring("""
#                                 S -> NP VP
#                                 PP -> P NP
#                                 NP -> Det N | Det N PP | 'I'
#                                 VP -> V NP | VP PP
#                                 Det -> 'an' | 'my'
#                                 N -> 'elephant' | 'pajamas'
#                                 V -> 'shot'
#                                 P -> 'in'
#                                 """)
# sent = 'I shot an elephant in my pajamas'
# sent = nltk.word_tokenize(sent)
# parser = nltk.ChartParser(groucho_grammar)

# #trees = parser.nbest_parse(sent)
# # AttributeError:'ChartParser' object has no attribute 'nbest_parse'
# trees = parser.parse(sent)
# # print(trees)
# for tree in trees:
#     print(tree)



# 上下文无关法

# grammar1 = CFG.fromstring("""
#                                 S -> NP VP
#                                 VP -> V NP | VP PP
#                                 PP -> P NP
#                                 V -> 'saw' | 'ate' | 'walked'
#                                 NP -> 'John' | 'Mary' | 'Bob' | Det N | Det N PP
#                                 Det -> 'a' | 'an' | 'the' | 'my'
#                                 N -> 'man' | 'dog' | 'cat' | 'telescope' | 'park'
#                                 P -> 'in' | 'on' | 'by' | 'with'
#                                 """)
# sent = 'Mary saw Bob'.split()
# rd_parser = nltk.RecursiveDescentParser(grammar1)       #递归下降解析器
# for tree in rd_parser.parse(sent):
#     print(tree)


# #编写自己的文法
# grammar1 = nltk.data.load('file:mygrammar.cfg')
# rd_parser = nltk.RecursiveDescentParser(grammar1)
# for tree in rd_parser.parse(sent):
#     print(tree)

# https://www.nltk.org/book/ch08.html

 	
def filter(tree):
    child_nodes = [child.label() for child in tree
                   if isinstance(child, nltk.Tree)]
    return  (tree.label() == 'VP') and ('S' in child_nodes)

groucho_grammar = nltk.CFG.fromstring("""
                                        S -> NP VP
                                        PP -> P NP
                                        NP -> Det N | Det N PP | 'I'
                                        VP -> V NP | VP PP
                                        Det -> 'an' | 'my'
                                        N -> 'elephant' | 'pajamas'
                                        V -> 'shot'
                                        P -> 'in'
                                        """)
 	
sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(groucho_grammar)
for tree in parser.parse(sent):
    print(tree)
    print(filter(tree))
    
    tree.draw()
# #上下文无关法
# def test_nltk_cfg_zh():
#     # https://github.com/Samurais/text-cfg-parser/blob/master/app/sample.py
#     print("test_nltk_cfg_zh")
#     grammar = nltk.CFG.fromstring("""
#         S -> N VP
#         VP -> V NP | V NP | V N
#         V -> "尊敬"
#         N -> "我们" | "老师" | "狗子"
#         """)

#     # Make your POS sentence into a list of tokens.
#     sent = "我们 尊敬 狗子".split()

#     # Load the grammar into the RecursiveDescentParser.
#     rd_parser = RecursiveDescentParser(grammar)

#     result = []

#     for i, tree in enumerate(rd_parser.parse(sent)):
#         result.append(tree)
#         print("Tree [%s]: %s" % (i + 1, tree))

#     assert len(result) > 0, "Can not recognize CFG tree."
#     if len(result) == 1 :
#         print("Draw tree with Display ...")
#         result[0].draw()
#     else:
#         print("WARN: Get more then one trees.")

#     print(result)
# test_nltk_cfg_zh()