#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
import re
sdict= '../../libs/dict.txt.big'
jieba.set_dictionary(sdict)
userdict= '../../libs/userdict.txt'
stop_words= '../../libs/stop_words.txt'
jieba.load_userdict(userdict)
def segment(sentence, cut_all=False):

    
    

    # jieba.analyse.set_stop_words(stop_words)
    sentence = sentence.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
    # sentence = ' '.join(jieba.cut(sentence, cut_all=cut_all))
    #jieba.cut_for_search 方法接受两个参数：需要分词的字符串；是否使用 HMM 模型。该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细
    sentence = ' '.join(jieba.cut_for_search(sentence))
    return re.sub('[a-zA-Z0-9.。:：,，)）(（！!??*-_/”“\"]', '', sentence).split()
