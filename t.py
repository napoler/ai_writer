# # from libs import TerrySearch
# # from libs import TerrySearch
# import libs
# import fun


# baiduai= libs.BaiduAi()

# title = "但性格非常稳健，完全没有一般 "

# content = """

# 1、发情母犬的阴唇肿胀、肥大、外突、初期粉红色，明显充血并有少量黏液伴随血液从母犬的阴道流出。随着发情期的延续，流出的血量逐日增加，血液的颜色也由粉红色变为深红色：发情的第8天，血量最多最浓，血色最深。第9天以后血量渐少，浓度渐稀，这时阴唇也逐渐变为暗红色。由于这时阴唇肿胀渐消，开始出现皱纹，发情的母犬进入了排卵期。排卵期大约持续5—6天，这时的发情母犬乐意接受公犬爬跨。随着排卵期的延伸，发情母犬的求爱表现日炽，直到发情期的第16天，母犬开始讨厌公犬纠缠、这时发情母犬的阴道仍有血水流出，到第21天时，阴道流血停止，阴唇肿胀消退，母犬发情结束。
# 2、发情期母犬表情兴奋。随着发情期的持续，母犬的兴奋增强，表情比平时恍惚不安，吠声粗大，双目发亮。发情炽期，母犬坐卧不安，食欲锐减，拴养的母犬不断对空发出求偶吠，养犬者这时如果用手按压母犬的腰部或抚摸犬尾时，母犬站立不动，或把犬尾偏向一侧，犬的阴唇不断抽动，并且阴门频频开启和闭合，这时如用性成熟的公犬试情时，发情的母犬后肢叉开，出现主动接受交配状。养犬者在犬的发情期，一定要密切观察发情母犬的上述变化和表情，一定要记住母犬发情开始（母犬阴道流血第一天）的日子，以便推算出该母犬最佳的交配日：只有在最佳交配日配种，才能提高母犬的受胎率和产仔数。
# 最佳配种日和配种

# """


# t = baiduai.topic(title,content)
# print(t)
# # t = baiduai.commentTag(content)
# # print(t)


# # -*- coding:utf-8 -*-
# Author：wancong
# Date: 2018-04-29
from pyhanlp import *


def demo_dependency_parser():
    """ 依存句法分析（CRF句法模型需要-Xms512m -Xmx512m -Xmn256m，
        MaxEnt和神经网络句法模型需要-Xms1g -Xmx1g -Xmn512m）
        https://github.com/hankcs/pyhanlp
    """
    sentence = HanLP.parseDependency("独立自己爱思考，加上无忧无虑爱冒险，可以很负责任的说，哈士奇是班级里成绩好，但不听老师管教的学生。")
#     print(dir())
#     for word in sentence.iterator():  # 通过dir()可以查看sentence的方法
# #         print(word.ID)
# #         print(word.HEAD.ID)
#         print((word.ID,word.LEMMA, word.DEPREL, word.HEAD.LEMMA,word.POSTAG,word.HEAD.ID))
#     print()

    # 也可以直接拿到数组，任意顺序或逆序遍历
    word_array = sentence.getWordArray()
    CoNLLWord = JClass("com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord")
    i= 0 
    for word in word_array:
#         print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
        print((i,word.LEMMA, word.DEPREL, word.HEAD.LEMMA,word.POSTAG,word.HEAD.ID))

        # head = word
        # while head.HEAD:
        #     head = head.HEAD
        #     if (head == CoNLLWord.ROOT):
        #         print(head.LEMMA)
        #     else:
        #         print("%s --(%s)--> " % (head.LEMMA, head.DEPREL))


        i=i+1
        
        pass
    print(len(word_array))

    # 还可以直接遍历子树，从某棵子树的某个节点一路遍历到虚根
    CoNLLWord = JClass("com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord")
    head = word_array[0]
    while head.HEAD:
        head = head.HEAD
        if (head == CoNLLWord.ROOT):
            print(head.LEMMA)
        else:
            print("%s --(%s)--> " % (head.LEMMA, head.DEPREL))

    # 还可以直接遍历子树，从某棵子树的某个节点一路遍历到虚根
    CoNLLSentence = JClass("com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLSentence")
    # head = word_array[0]
    # while head.HEAD:
    #     head = head.HEAD
    #     if (head == CoNLLSentence.ROOT):
    #         print(head.LEMMA)
    #     else:
    #         print("%s --(%s)--> " % (head.LEMMA, head.DEPREL))
if __name__ == "__main__":
    demo_dependency_parser()
#     import doctest
#     doctest.testmod(verbose=True, optionflags=doctest.NORMALIZE_WHITESPACE)




