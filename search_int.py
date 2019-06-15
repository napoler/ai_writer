# from libs import TerrySearch
import libs

#开始运行
#新的搜索
# libs.TerrySearch().init_search()
#索引目录
libs.TerrySearch().start(path='/home/terry/pan/github/ai_writer/ai_writer/data/kw2text/')
#搜索

# import jieba
text ="近日，由国际环保组织野生救援"
# seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
# # print(", ".join(seg_list))
# text=" ".join(seg_list)
r= libs.TerrySearch().search(text=text)
print(r)
