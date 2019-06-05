# 导入 webdriver

import logging
import synonyms

from cacheout import Cache
cache = Cache()

class RewritStatement:
    """这里重写语句
    基于同义词 https://github.com/huyingxi/Synonyms
    """
    def __init__(self):
        """开始初始化搜索
        """
        pass
    def text(self,text):

        # text="可以用于自然语言理解的很多任务"
        kws,s = synonyms.seg(text)
        # kws =tkit.Text().get_keywords(text,num=3)
        # l = {'n','nz','ns','nr'}
        # kws_new = []
        keyword =''
        # for key,item in enumerate(s):
        #     print(key)
        #     print(item)

        #     print(kws[key])
        #     if item in l:
        #         keyword = keyword+" "+kws[key]

        new = ''
        for key,item in enumerate(s):
            # print(key)
            # print(item)

            # print(kws[key])
            # if item in l:
            #     keyword = keyword+" "+kws[key]
            kn,p= synonyms.nearby(kws[key])
            print(kn)
            print(p)
            if len(kn)>1 and p[1]>0.8:

                print(kn[1])
                # if p[1]>0.7:
                print('建议选择')
                new = new + kn[1]
            else:
                new = new + kws[key]
        return new
        # print(text)        
        # print(new)