import jieba
import jieba.analyse
import jieba.posseg as pseg


class Keyword:

    # empCount = 0

    def __init__(self,idf_path = "./libs/idf.txt",stop_words = "./libs/stop_words.txt",userdict = "./libs/userdict.txt",sdict = "./libs/dict.txt.big",withWeight = True,topK= 50,allowPOS= ()):
        print('开始获取关键词')
        # topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
        # withWeight 为是否一并返回关键词权重值，默认值为 False
        # allowPOS 仅包括指定词性的词，默认值为空，即不筛选
        self.topK= topK
        self.idf_path = idf_path
        self.stop_words = stop_words
        self.userdict = userdict
        self.dict = sdict
        self.withWeight = withWeight
        self.allowPOS= allowPOS
        # self.allowPOS= ('ns', 'n', 'vn', 'v')  
        jieba.analyse.set_idf_path(self.idf_path)
        jieba.set_dictionary(self.dict)
        jieba.load_userdict(self.userdict)
        jieba.analyse.set_stop_words(self.stop_words)

    def get_keyword(self,text):

        
        tags = jieba.analyse.extract_tags(text, topK=self.topK ,withWeight=self.withWeight, allowPOS=self.allowPOS)

        # print(",".join(tags))
        return tags
    def get_keyword_list(self,text):
        items = []
        for word,ran in self.get_keyword(text):
            items.append(word)
        return items

    def get_keyword_pseg(self,text):
        # jieba.analyse.set_idf_path(self.idf_path)
        # jieba.load_userdict(self.userdict)
        # jieba.set_dictionary(self.dict)
        # jieba.analyse.set_stop_words(self.stop_words)
        words = pseg.cut(text)
        for word, flag in words:
            print('%s %s' % (word, flag))

# k=Keyword()
# text= ""
# print(k.get_keyword(text))