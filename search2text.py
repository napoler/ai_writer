"""
搜索文章分类数据,构建训练数据



"""
import libs
from tqdm import tqdm
import os,random
import shutil
import argparse

ARTICLE_PATH ="./data/kw2text_mini/"
KWFILE= 'keywords.txt' #一行一个关键词
# KWLIST= ['狗','猫','宠物','动物','植物']

def run():
        """ 
        >>> python3 search2text.py --text 犬
        """
        #     baiduai= libs.BaiduAi()
        #     parser = argparse.ArgumentParser(description='python3 search2text.py --text 犬')
        #     parser.add_argument('--text', type=str, default = None)
        #     #需要搜索的关键词

        #     args = parser.parse_args()
        # import libs
        model ="/home/terry/pan/github/bert/model/last_xiangguan/"
        

        #     text =args.text
        with open(KWFILE) as  f1:#
                keywords = f1.readlines()
                keywords_new=[]
                for keyword in keywords:
                        keywords_new.append(keyword)
        random.shuffle(keywords_new)
        print(keywords_new)
        for keyword in keywords_new:
                r= libs.TerrySearch().search(text=keyword,limit=10000)
                # print(len(r))
                to =ARTICLE_PATH
                
                # for item in tqdm(r):
                other = 0
                i = 0
                cf= libs.Classifier(model)
                for item in r:
                        if i%2 == 0:
                                #释放显存和内存
                                cf.free_ram()
                                cf= libs.Classifier(model)

                        # print(item['data']['content'])
                        print(item['data']['title'])

                        # print(item['data']['path'])

                        # t = baiduai.topic(item['data']['title'],item['data']['content'])
                        if item['data']['content']:
                                try:    
                                        t =cf.proportion_article_auto(item['data']['content'])
                                # print(item['data']['title'])
                                except:
                                        continue

                                print(item['data']['path'])
                                print(t)
                                if t[0]['label']==1:
                                        print("宠物内容")

                                        try:    
                                                print('开始复制文件')
                                                shutil.copy(item['data']['path'], to)
                                        except:
                                                pass
                                        # continue
                                else:
                                        print("其它内容")
                                        if other> 200:
                                                print("不相干内容过多自动跳出")
                                                break
                                        
                                        other = other+1
                        i = i+1
                        # cf.free_ram()

                print("运行搜索任务完成!!!!!!!")
                                
 
                                        

if __name__=='__main__':
    run()
