# from libs import TerrySearch
import libs

#开始运行
#新的搜索
# libs.TerrySearch().init_search()
#libs.TerrySearch().start(path='/home/terry/pan/github/terry_search_web/terry_search_web/data/article/')
libs.TerrySearch().start(path='/home/terry/pan/github/terry_search_web/terry_search_web/data/wiki/')
#搜索

# import jieba
text ="近日，由国际环保组织野生救援"
# seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
# # print(", ".join(seg_list))
# text=" ".join(seg_list)
r= libs.TerrySearch().search(text=text)
print(r)
