from fun import *
import json
import libs
from MicroHMM.hmm import HMMModel

from tqdm import tqdm
def train():
    model_dir_str="data/hmm"
    hmm_model = HMMModel()
    output='/home/terry/pan/github/Bert-Sentence-streamlining/Bert-Sentence-streamlining/data/train_old.json'
    with open(output,'r') as f:
        
        items=[]
        for line in tqdm(f):
            j_content = json.loads(line)
            if j_content['label']=="Yes":
                items.append(j_content)
                one_line=bulid_mark(j_content['sentence'])
                # print(j_content['sentence'])
                # print(one_line)
                hmm_model.train_one_line(one_line)
        hmm_model.save_model(model_dir_str)
    text="它们的岗位，一只边牧可以管理上千头羊群呢，它们为主人忠心耿耿的守护着家畜，守护着家园"
    s=jieba_seg_list(text)
    result = hmm_model.predict(s)
    print(result)
    print(hmm_model)


def load():
    model_dir_str="data/hmm"
    
    # hmm_model = HMMModel()
    hmm_model =HMMModel.load_model(model_dir=model_dir_str)
    print(hmm_model)
    text="它们"
    s=jieba_seg_list(text)
    result = hmm_model.predict(s)
    print(result)
# train()

load()

# hmm_model = HMMModel()
# # one_line = [('当然', 'No'), ('了', 'Yes'), ('，', 'No'), ('依然', 'No'), ('还有', 'No'), ('不少', 'No'), ('的', 'No'), ('边境牧羊犬', 'No'), ('活跃', 'No'), ('在', 'No'), ('野外', 'No'), ('、', 'No'), ('牧场', 'No'), ('，', 'No'), ('在', 'No'), ('那些', 'No'), ('畜牧业', 'No'), ('发达', 'No'), ('的', 'No'), ('国家', 'No'), ('，', 'No'), ('坚守', 'No'), ('着', 'No'), ('它们', 'No'), ('的', 'No'), ('岗位', 'No'), ('，', 'No'), ('一只', 'No'), ('边牧', 'No'), ('可以', 'No'), ('管理', 'No'), ('上', 'No'), ('千头', 'No'), ('羊群', 'No'), ('呢', 'Yes'), ('，', 'No'), ('它们', 'No'), ('为主', 'No'), ('人', 'No'), ('忠心耿耿', 'No'), ('的', 'No'), ('守护', 'No'), ('着', 'No'), ('家畜', 'No'), ('，', 'No'), ('守护', 'No'), ('着', 'No'), ('家园', 'No')]
# text1="""

# ##del##西伯利亚##del##雪橇犬是原始的古老犬种，主要生活在在西伯利亚##del##东北部##del##、格陵兰南部。哈士奇名字是源自其独特的嘶哑叫声 [1]  。哈士奇性格多变，有的极端胆小，也有的极端暴力，进入人类社会和家庭的哈士奇，都已经没有了这种极端的性格，比较温顺，是一种流行于全球的宠物犬。哈士奇、金毛犬与拉布拉多并列为三大无攻击性犬类 [2]  ，被世界各地人们广泛饲养，并在全球范围内有大量该犬种的赛事。
# """
# one_line=bulid_mark(text1)
# hmm_model.train_one_line(one_line)
# print(hmm_model)
# # text="当然了，依然还有不少的边境牧羊犬活跃在野外、牧场，在那些畜牧业发达的国家，坚守着它们的岗位，一只边牧可以管理上千头羊群呢，它们为主人忠心耿耿的##del##守护##del##着家畜，守护着家园"
# text="""
# ##del##
# 西伯利亚雪橇犬是原始的古老犬种，主要生活在在西伯利亚东北部、格陵兰南部。哈士奇名字是源自其独特的嘶哑叫声 [1]  。哈士奇性格多变，有的极端胆小，也有的极端暴力，进入人类社会和家庭的哈士奇，都已经没有了这种极端的性格，比较温顺，是一种流行于全球的宠物犬。哈士奇、金毛犬与拉布拉多并列为三大无攻击性犬类 [2]  ，被世界各地人们广泛饲养，并在全球范围内有大量该犬种的赛事。
# """
# s=jieba_seg_list(text)
# result = hmm_model.predict(s)
# print(result)