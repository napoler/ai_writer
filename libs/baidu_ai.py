# -*- coding: utf-8 -*-
from aip import AipNlp
import configparser

config = configparser.ConfigParser()

config.read("./config/config.ini")


class BaiduAi:
    """百度ai接口
    https://ai.baidu.com/docs#/NLP-Python-SDK/f524c757
    """

    # empCount = 0

    def __init__(self):
        print('kaishi')
        # print(config.get('site', 'name'))
        self.app_id = config.get('baidu', 'app_id')
        self.api_key = config.get('baidu', 'app_key')
        self.secret_key = config.get('baidu', 'secret_key')
        self.client = AipNlp(self.app_id, self.api_key, self.secret_key)
        # """ 你的 APPID AK SK """
    def lexer(self, text):
        """ 调用词法分析
        """

        return self.client.lexer(text)


    def depParser(self, text):
        """依存句法分析
        
        """

        return self.client.depParser(text)


    def dnn(self, text):


        
        # result = client.synthesis(text, 'zh', 1, {
        #     'vol': 11,
        # })
        # text = "床前明月光"

        # """ 调用DNN语言模型 """
        # print(client)
        return self.client.dnnlm(text)
    def wordSimEmbedding(self,text1, text2):
        """ 词义相似度
        
        """
        return self.client.wordSimEmbedding( text1, text2)
    def simnet(self,text1, text2):
        """ 短文本相似度 
        
        """
        return self.client.simnet( text1, text2)
    def commentTag(self,content):
        """ 评论观点抽取
        
        """
        return self.client.commentTag( content)

    def topic(self,title,content):
        """ 调用文章分类 
        
        """
        try:
            return self.client.topic(title, content)
        except:
            return {'log_id': 8348398184393122510, 'item': {'lv2_tag_list': [], 'lv1_tag_list': []}}
            
    def keyword(self,title,content):
        """ 文章标签
        文章标签服务能够针对网络各类媒体文章进行快速的内容理解，根据输入含有标题的文章，输出多个内容标签以及对应的置信度，用于个性化推荐、相似文章聚合、文本内容分析等场景。
        
        """
        return self.client.keyword(title, content)
    def sentimentClassify(self,content):
        """情感倾向分析
        对包含主观观点信息的文本进行情感极性类别（积极、消极、中性）的判断，并给出相应的置信度。
        
        """

        return self.client.sentimentClassify(content)
    def ecnet(self,content):
        """智能纠错
        
        """

        return self.client.ecnet(content)

    def newsSummary(self,title,content):
        """生成摘要
        暂时无权限
        """

        return self.client.newsSummary(content, 200)
