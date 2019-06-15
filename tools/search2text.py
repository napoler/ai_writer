import libs
from tqdm import tqdm
import os
import shutil
import argparse

ARTICLE_PATH ="./data/kw2text_mini/"
KWFILE= 'keywords.txt' #一行一个关键词
KWLIST= ['狗','猫','宠物','动物','植物']
def run():
    """ 
    >>> python3 search2text.py --text 犬
    """
    baiduai= libs.BaiduAi()
#     parser = argparse.ArgumentParser(description='python3 search2text.py --text 犬')
#     parser.add_argument('--text', type=str, default = None)
#     #需要搜索的关键词

#     args = parser.parse_args()
# import libs
model ="/home/terry/pan/github/bert/model/last_xiangguan/"
cf= libs.Classifier(model)
#     text =args.text
    with open(KWFILE) as  f1:#
        keywords = f1.readlines()
        for keyword in keywords:
                r= libs.TerrySearch().search(text=keyword,limit=1000)
                # print(len(r))
                to =ARTICLE_PATH
                
                # for item in tqdm(r):
                for item in r:
 
                        # print(item['data']['content'])
                        print(item['data']['title'])

                        # print(item['data']['path'])
  
                        t = baiduai.topic(item['data']['title'],item['data']['content'])
                        if 'item' in t:
                    
                                # print(t)
                                # if len(t['item']['lv2_tag_list'])>0:
                                if 'lv2_tag_list' in t:

                                        new_tag_list = t['item']['lv2_tag_list'] +t['item']['lv1_tag_list']
                                else:
                                        new_tag_list = t['item']['lv1_tag_list']
                                for tag in new_tag_list:
                                        print(tag)
                                        if tag['tag'] in KWLIST:
                                                print ('数据为宠物相关')
                                                print(item['data']['title'])

                                                print(item['data']['path'])
                                                try:    
                                                        print('开始复制文件')
                                                        shutil.copy(item['data']['path'], to)
                                                except:
                                                        pass
                                                continue
                                        

if __name__=='__main__':
    run()
