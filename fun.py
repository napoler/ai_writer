from flask import Flask, render_template, request, json, Response, jsonify
import jieba
jieba.load_userdict("libs/userdict.txt")
import sqlite3
import csv,re
import Terry_toolkit as tkit
import libs
from random import choice
import random
import gc,os
import subprocess
import hashlib
import time
import shutil
from bert_sample import SentencePrediction,MaskedLM
import configparser
config = configparser.ConfigParser()

config.read("./config/config.ini")



from random import sample
# from MagicBaidu import MagicBaidu


def terry_cache_key(fun_name,text):
    md5_val = hashlib.md5(text.encode('utf8')).hexdigest()
    key=fun_name+str(md5_val)
    return key

def run_auto_sort(text,id):
    cmd="python3 bert_run_jianxie.py --do auto_sort --id '''"+id+"''' --text '''"+text+"'''"

    e = subprocess.call(cmd, shell=True)
    return e 
# def auto_sort(text,id):
#     nextS=SentencePrediction()
#     mod= config.get('bert', 'model')
#     nextS.model_init(model=mod)
#     t_text=tkit.Text()
#     text_list=t_text.sentence_segmentation(text)
#     print(text_list)
#     text_list_mini=t_text.sentence_segmentation(text)
#     # new_text='。'.join(text_list_mini)
#     # print('new_text',new_text)
#     l=[]
#     next_s=random.choice(text_list)
#     Article=next_s
#     print('文章开始:+++++++++++++')
#     for i in range(0,len(text_list)):
#         # print(line)
#         print(next_s)

#         if len(text_list_mini)>1:
#             text_list_mini.remove(next_s)
#             new_text='。'.join(text_list_mini)
#             # print('new_text',new_text)
#             next_line=nextS.sentence(new_text,next_s)
#             # print(next_line)
#             if len(next_line)>0:
#                 next_s=next_line[0]['line_to_check']
#                 # print(next_s)
#                 # l.append(next_line[0])
#                 Article=Article+'。'+next_s

#         elif len(text_list_mini)==1:
#             Article=Article+'。'+text_list_mini[0]+'。'
#             break

#             # l.append(next_line[0])
#     # print(l)
#     # data ={
#     #     'start':next_s
#     #     'next':sentence
#     # }
#     # print(Article)
#     save_article_plus(Article,id)
#     return 
#     pass

def baidu_search(keyword):
    # mb = MagicBaidu()
    # l=[]
    # for i in mb.search(query=keyword):
    #     try:
    #         # print(i)
    #         l.append(i)
    #     except:
    #         pass
    l = run_baidu(keyword)
    print(l)
    return l
    # bsearch = libs.BaiduSearch()
    # lis,kws = bsearch.search(keyword=keyword,num = 2)
    # print(lis,kws)
# baidu_search('柯基犬')
def url_text(url):
    ut = libs.UrlText()
    print(url)
    text = ut.get_text(url)
    print(text)
        #将文本保存
    # 
    if len(text)>0:
            
        save_article_add_search(text)
        data={
            'data':text,
            'state':'success'
        }


        
    else:
        data={
            'data':'',
            'state':'fail'
        }
    print(data)
    return data
# a = url_text("https://movie.douban.com/subject/30441625/")
# print(a)
def get_post_data():
    """
    从请求中获取参数
    :return:
    """
    data = {}
    if request.content_type.startswith('application/json'):
        data = request.get_data()
        data = json.loads(data)
    else:
        for key, value in request.form.items():
            if key.endswith('[]'):
                data[key[:-2]] = request.form.getlist(key)
            else:
                data[key] = value
    return data

def save_article(text):
    # 存储单篇文章
    # ARTICLE_PATH
    #text = 'kngines'
    md5_val = hashlib.md5(text.encode('utf8')).hexdigest()

    articlefile= 'article_'+str(md5_val)+'.txt'
    if os.path.isfile(ARTICLE_PATH+articlefile):
        print("文件已经存在跳过")
    else:
        my_open = open(ARTICLE_PATH+articlefile, 'a')
        my_open.write(str(text)+'\n\n')
        my_open.close()

def save_article_add_search(text):
    # 存储单篇文章
    # ARTICLE_PATH
    #text = 'kngines'
    md5_val = hashlib.md5(text.encode('utf8')).hexdigest()

    articlefile= 'article_'+str(md5_val)+'.txt'
    if os.path.isfile('./data/kw2text_mini/'+articlefile):
        print("文件已经存在跳过")
    else:
        my_open = open('./data/kw2text_mini/'+articlefile, 'a')
        my_open.write(str(text)+'\n\n')
        my_open.close()
        # 添加文件到本地搜索
        libs.TerrySearch().add_one('./data/kw2text_mini/'+articlefile)



def save_article_plus(text,id):
    # 存储单篇文章
    # ARTICLE_PATH
    #text = 'kngines'
    # md5_val = hashlib.md5(text.encode('utf8')).hexdigest()

    articlefile= './data/article/'+id+'.txt'
    # if os.path.isfile(ARTICLE_PATH+articlefile):
    #     print("文件已经存在跳过")
    # else:
    my_open = open(articlefile, 'w+')
    my_open.write(str(text)+'')
    my_open.close()
    print("内容已经保存"+id)
    return
def get_article_plus(id):
    # 获取单篇文章
    # ARTICLE_PATH
    #text = 'kngines'
    # md5_val = hashlib.md5(text.encode('utf8')).hexdigest()

    articlefile= './data/article/'+id+'.txt'
    tfile =  tkit.File()
    t_text=tkit.Text()
    text=tfile.open_file(articlefile)
    print("内容获取成功"+id)
    text_list=t_text.sentence_segmentation(text)
    # data ={
    #     'text_list':text_list
    # }
    return text_list

def move_used(id):
    # 转移已经使用的文本
    # ARTICLE_PATH
    #text = 'kngines'
    # md5_val = hashlib.md5(text.encode('utf8')).hexdigest()

    articlefile= './data/article/'+id+'.txt'
    used= './data/article_used'
    shutil.move(articlefile, used)  # 移动
    return 
def bulid_mark(text):
    """添加一条数据"""
    tfile =  tkit.File()
    t_text=tkit.Text()
    # print(text)

    p=re.compile(r'[##del##](.*?)[##del##]',re.S)
    words= re.findall(p, text)
    # 获取标记后的关键词
    words = remove_null(words)
    # s=re.split(r'##del##',text)
    # text= ''.join(s)
    text= text.replace("##del##", "")

    # for word in words:
    seg_list=jieba_seg_list(text)
    # print(seg_list)
    new=[]
    for i,item in enumerate(seg_list):
        # print(item)
        s=jieba_seg_list(text)
        calculate='No'
        while item in words:
            words.remove(item)
            calculate='Yes'
        # s[i]=(item,calculate)
        new.append((item,calculate))
    return new

     
def add_sentence_one_unmark(text):
    """添加一条未标记的数据"""
    tfile =  tkit.File()
    t_text=tkit.Text()
    print(text)

    p=re.compile(r'[##del##](.*?)[##del##]',re.S)
    words= re.findall(p, text)
    # 获取标记后的关键词
    words = remove_null(words)
    # s=re.split(r'##del##',text)
    # text= ''.join(s)
    text= text.replace("##del##", "")

    # for word in words:
    seg_list=jieba_seg_list(text)
    print(seg_list)
    seg_list_unmark=seg_list
    print('words',words)
    for word in words:
        try:
            seg_list_unmark.remove(word)
        except:
            print('无法移除',word)
            pass
    

    seg_list_unmark_mini=sample(seg_list_unmark, len(words)) # 随机抽取和已经标记相同数目的样本
    print('seg_list_unmark_mini',seg_list_unmark_mini)
    for i,item in enumerate(seg_list):
        # print(item)
        s=jieba_seg_list(text)
        s2=jieba_seg_list(text) #第二种
        calculate='ignore'

        #这里是抽取未标记的生成
        while item in seg_list_unmark_mini:
            # s=re.split(r'##del##',text)
            # print('s',s)
            seg_list_unmark_mini.remove(item)
            calculate='No'

        # while item in words:
        #     # s=re.split(r'##del##',text)
        #     # print('s',s)
        #     words.remove(item)
        #     calculate='Yes'
        # # if calculate=='Yes':

        # else:
        # new= ch_one(item,s)
        s[i]="##del##"+item+"##del##"
        s2[i]="###" #第二种
        # del(s)
        # print(new)
        data={
            'label':calculate,
            'sentence':''.join(s)

        }
        data2={
            'label':calculate,
            'sentence':''.join(s2)

        }
        # print(data)
        if calculate=='ignore' :
            # 未选择忽略
            # libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
            pass
        else:
            libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
            # print(data)
            libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train_v2.json',data2)


def replace_mark(words,text):
    """
    生成标记词语
    """
    new=[]
    for word in words:
        t= text.replace("##del##"+word+"##del##", "[mark]"+word+"[mark]").replace("##del##", "").replace("[mark]"+word+"[mark]", "##del##"+word+"##del##")
        new.append(t)
    # print(new)
    text_clear= text.replace("##del##", "")


    seg_list=jieba_seg_list(text_clear)
    s_list=[]
    m_list=[]
    for i,item in enumerate(seg_list):
        s=jieba_seg_list(text_clear)
        s[i]="##del##"+item+"##del##"
        calculate="No"
        while ''.join(s) in new:
            calculate="Yes"
            # print("标记内容")
            break

        data={
            'label':calculate,
            'sentence':''.join(s)

        }
        if calculate=="Yes":
            m_list.append(data)
        else:
            s_list.append(data)
        print(data)
        # libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
        #随机产生一条
        # random_sentence_one()
    last={
        'mark':m_list,
        'unmark':s_list
        
    }

    return last
def add_sentence_one(text):
    """添加一条数据"""
    tfile =  tkit.File()
    t_text=tkit.Text()
    print(text)

    p=re.compile(r'[##del##](.*?)[##del##]',re.S)
    words= re.findall(p, text)
    # 获取标记后的关键词
    words = remove_null(words)
    ls= replace_mark(words,text)
    mark_list= ls['mark']
    # if len(ls['unmark'])>len(ls['mark']):
    #     unmark_list=sample(ls['unmark'], len(ls['mark']))
    # else:
    #     unmark_list=ls['unmark']
    unmark_list=ls['unmark']
    new_list=mark_list+unmark_list
    for item in new_list:
        libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',item)
                #随机产生一条
        # random_sentence_one()









    # text= text.replace("##del##", "")

    # # for word in words:
    # seg_list=jieba_seg_list(text)
    # print(seg_list)
    # seg_list_unmark=seg_list
    # print('words',words)
    # for word in words:
    #     try:
    #         seg_list_unmark.remove(word)
    #     except:
    #         print('无法移除',word)
    #         pass

    # seg_list_unmark_mini=sample(seg_list_unmark, len(words)) # 随机抽取和已经标记相同数目的样本
    # print('seg_list_unmark_mini',seg_list_unmark_mini)


    # for i,item in enumerate(seg_list):
    #     print(item)
    #     s=jieba_seg_list(text)
    #     s2=jieba_seg_list(text) #第二种
    #     calculate='ignore'

    #     #这里是抽取未标记的生成
    #     while item in seg_list_unmark_mini:
    #         # s=re.split(r'##del##',text)
    #         # print('s',s)
    #         seg_list_unmark_mini.remove(item)
    #         calculate='No'

    #     while item in words:
    #         # s=re.split(r'##del##',text)
    #         # print('s',s)
    #         words.remove(item)
    #         calculate='Yes'
    #     # if calculate=='Yes':

    #     # else:
    #     # new= ch_one(item,s)
    #     s[i]="##del##"+item+"##del##"
    #     s2[i]="###" #第二种
    #     # del(s)
    #     # print(new)
    #     data={
    #         'label':calculate,
    #         'sentence':''.join(s)

    #     }
    #     data2={
    #         'label':calculate,
    #         'sentence':''.join(s2)

    #     }
    #     print(data)
    #     if calculate=='ignore' :
    #         # 未选择忽略
    #         # libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
    #         pass
    #     else:
    #         libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
    #         # print(data)
    #         libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train_v2.json',data2)
    # #随机产生一条
    # random_sentence_one()


# def add_sentence_one(text):
#     """添加一条数据"""
#     tfile =  tkit.File()
#     t_text=tkit.Text()
#     print(text)

#     p=re.compile(r'[##del##](.*?)[##del##]',re.S)
#     words= re.findall(p, text)
#     # 获取标记后的关键词
#     words = remove_null(words)
#     # s=re.split(r'##del##',text)
#     # text= ''.join(s)
#     text= text.replace("##del##", "")

#     # for word in words:
#     seg_list=jieba_seg_list(text)
#     print(seg_list)
#     seg_list_unmark=seg_list
#     print('words',words)
#     for word in words:
#         try:
#             seg_list_unmark.remove(word)
#         except:
#             print('无法移除',word)
#             pass
    
#     replace_mark(words,text)
#     seg_list_unmark_mini=sample(seg_list_unmark, len(words)) # 随机抽取和已经标记相同数目的样本
#     print('seg_list_unmark_mini',seg_list_unmark_mini)


#     for i,item in enumerate(seg_list):
#         print(item)
#         s=jieba_seg_list(text)
#         s2=jieba_seg_list(text) #第二种
#         calculate='ignore'

#         #这里是抽取未标记的生成
#         while item in seg_list_unmark_mini:
#             # s=re.split(r'##del##',text)
#             # print('s',s)
#             seg_list_unmark_mini.remove(item)
#             calculate='No'

#         while item in words:
#             # s=re.split(r'##del##',text)
#             # print('s',s)
#             words.remove(item)
#             calculate='Yes'
#         # if calculate=='Yes':

#         # else:
#         # new= ch_one(item,s)
#         s[i]="##del##"+item+"##del##"
#         s2[i]="###" #第二种
#         # del(s)
#         # print(new)
#         data={
#             'label':calculate,
#             'sentence':''.join(s)

#         }
#         data2={
#             'label':calculate,
#             'sentence':''.join(s2)

#         }
#         print(data)
#         if calculate=='ignore' :
#             # 未选择忽略
#             # libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
#             pass
#         else:
#             libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
#             # print(data)
#             libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train_v2.json',data2)
#     #随机产生一条
#     random_sentence_one()


    # for word in words:
    #     #随机产生一条
    #     random_sentence_one()
    #     s=re.split(r'##del##',text)
    #     print('s',s)
    #     new= ch_one(word,s)
    #     calculate='Yes'
    #     data={
    #         'label':calculate,
    #         'sentence':''.join(new)

    #     }
    #     print(data)
    #     libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
    # for word in words:
    #     #随机产生一条
    #     random_sentence_one()
    #     s=re.split(r'##del##',text)
    #     print('s',s)
    #     new= ch_one(word,s)
    #     calculate='Yes'
    #     data={
    #         'label':calculate,
    #         'sentence':''.join(new)

    #     }
    #     print(data)
    #     libs.Terry().c_inputfile('/home/terry/github/ai_writer/ai_writer/data/mark/train.json',data)
def ch_one(word,list):
    """替换元素"""
    for i,item in enumerate(list):
        if item ==word:
            list[i]="##del##"+word+"##del##"

    return list

def remove_null(words):
    """删除空元素"""
    while '' in words:
        words.remove('')
    # print(words)
    return words




    # word = choice(seg_list)
    # print(seg_list)
    # seg_list_len = len(seg_list)
    # #判断句子是否是过短 过短则忽略
    # if seg_list_len> 3:
    #     pass
def jieba_seg_list(text):
    #对句子进行分词
    seg_list=[]
    for it in jieba.cut(text, cut_all=False):
    # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    # print()
        seg_list.append(it)
    return seg_list
def random_sentence_one():
    """
    随机生成一条未标记数据
    """
    # 获取未处理的数据
    tfile =  tkit.File()
    t_text=tkit.Text()
    # file_path="/home/terry/pan/github/ai_writer/ai_writer/data/kw2text_mini/"
    file_path="/home/terry/pan/github/ai_writer/ai_writer/data/kw2text/"
    file_list=tfile.file_List(file_path)
    f = choice(file_list)
    text = tfile.open_file(f)

    text_array= t_text.sentence_segmentation(text)
    sentence_one = choice(text_array)
    # sentence_one
    #对句子进行分词
    seg_list=jieba_seg_list(sentence_one)

    # word = choice(seg_list)
    seg_list_len = len(seg_list)
    #判断句子是否是过短 过短则忽略
    if seg_list_len> 3:
        # 随机整数：
        n = random.randint(0,seg_list_len-1)

        # seg_list
        # print(sentence_one)
        # print(seg_list)

        # a = ''.join(seg_list[0:n])
        # b = ''.join(seg_list[n])
        # if n ==seg_list_len:
        #     c = ''
        # else:
        #     c = ''.join(seg_list[n+1:seg_list_len])

        # full = a +'##del##'+b+'##del##'+c
        seg_list[n]= '##del##'+seg_list[n]+'##del##'
        full=''.join(seg_list)
        calculate='No'

        data={
            'label':calculate,
            'sentence':full

        }
        print(data)
        libs.Terry().c_inputfile('corpus.json',data)



def c_list(text):
    """
    创建预测所用的资料
    """
    seg_list=jieba_seg_list(text)

    l=[]
    for i,item in enumerate(seg_list):
        print(item)
        s=jieba_seg_list(text)
        calculate='No'

        s[i]="##del##"+item+"##del##"
        l.append(''.join(s))
    return l,seg_list




def yuce(text):
    # model ="/mnt/data/dev/model/bert-rewrite-sentences/"
    # cf= libs.Classifier(model)

    # # text_list="""
    # # 其返回值就是要统计参数出现的次数。在应用的时候最好是把列表赋给一个变量，之后再用count()方法来操作比较好。

    # # 当对象是一个嵌套的列表时，要查找嵌套列表中的列表参数count()方法同样可以完成。
    # # 體型酷似野狼，嚎叫的聲音亦與狼族無差，帶有特色的水藍眼睛，為西伯利亞哈士奇給人的第一印象。不知道哈士奇犬的人，首先的印象還是『狼犬』，近而產生害怕的心態，避之唯恐不及。不過，在了解哈士奇犬的人的心中，卻為這種外型俊秀、體態優美、笑容甜美的犬種所深深吸引，也使得這種在原產地擔任負重工作的工作犬，在其他地區搖身一變，成為同好間的賞玩、陪伴犬了！

    # #         一般人印象之中的哈士奇多為雪撬犬，在北極圈附近背負重物，拖曳雪橇，然而，在人類手下工作討生活的犬種並不只哈士奇犬，尚有阿拉斯加雪橇犬〈瑪拉幕帝犬〉、愛斯基摩犬及薩摩耶犬等三種，但在世人心中，雪橇犬就是哈士奇犬，哈士奇犬就是雪橇犬。其實上述四種犬種，在萬年前均有血緣關係，而哈士奇犬和薩摩耶犬的雪緣關係更為接近，在輾轉遷移過後，為適應當地環境，在體型、外貌上漸有轉變，如今只有哈士奇犬

    # # 與阿拉斯加犬在外型上極為相似，但在體型上就差一大截了！

    # # 西伯利亞哈士奇犬〈Siberian Husky〉，從字面上來看，Siberian代表此種犬來自西伯利亞地區，為當地原生犬種。一直到十八世紀，有艘遇暴風雨漂流至西伯利亞的日本船，船員發現當地土著楚奇克人飼養一種狗，這便是哈士奇犬首次為外界所知。Husky則是因為哈士奇犬的叫聲低沉嘶啞，便稱此種犬為哈士奇犬；另一種講法則是阿拉斯加淘金客在駕馭雪橇時發出Husky的聲音  〈意指沙啞的喊聲〉 ，而讓牠取得此種犬名。
    # # 节肢动物门（Arthropoda）蛛形纲（Arachnida）蜘蛛目（Araneida或Araneae）所有种的通称。除南极洲以外，全世界分布。从海平面分布到海拔5,000米处。
    # # 蜘蛛是陆地生态系统中最丰富的捕食性天敌，在维持农林生态系统稳定中的作用不容忽视。 [1]  体长1～90毫米，身体分头胸部（前体）和腹部（后体）两部分，头胸部覆以背甲和胸板。头胸部有附肢两对，第一对为螯肢，有螯牙、螯牙尖端有毒腺开口；直腭亚目的螯肢前后活动，钳腭亚目者侧向运动及相向运动；第二对为须肢，在雌蛛和未成熟的雄蛛呈步足状，用以夹持食物及作感觉器官；但在雄性成蛛须肢末节膨大，变为传送精子的交接器。
    # # 蜘蛛多以昆虫、其他蜘蛛、多足类为食，部分蜘蛛也会以小型动物为食。跳蛛视力佳，能在30厘米内潜近捕获猎物。
    # # 人们普遍认为蜘蛛是一种昆虫，但它们和蝎子、蜈蚣一样，不属于昆虫。因为昆虫的基本特征是体躯三段头、胸、腹，2对翅膀与6只足。 [2]
    # # 中文学名 蜘蛛 拉丁学名 Araneida；Araneae 别    称 网虫、扁蛛、园蛛、八脚螅、喜子、波丝。 界 动物界 门 节肢动物门 Arthropoda

    # # """


    # text_list,word_list = c_list(text)
    # print(text_list)
    # # word_list=jieba_seg_list(text)
    # print(word_list)
    # new_word=[]
    # data=[]
    # for i,item in enumerate(text_list):

    #     # print(item)

    #     t =cf.prediction(item)


    #     # print()
    #     print(t)
    #     r= word_list[i]
    #     if t[0]==0 :
    #         print('\n删除:'+word_list[i])
    #         # while r in word_list:
    #         #     word_list.remove(r)
    #         word ={
    #             'word':word_list[i],
    #             'remove':"Yes"

    #         }
    #     else:
    #         new_word.append(word_list[i])
    #         word ={
    #             'word':word_list[i],
    #             'remove':"No"

    #         }
    #     data.append(word)
    # print(text)
    # print("".join(new_word))
    # print(data)
    # del model
    # gc.collect()
    """
    执行命令行运行函数
    这里是简化
    """
    output = './data/jianxie'+str(time.time())+'.json'
    cmd="../bin/python3 bert_run_jianxie.py --do jianxie --output "+output+' --text """'+text+'"""'
    print(cmd)
    # cmd="python3 bert_run_jianxie.py --text "+text
    # output = './data/jianxie.json'
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    return data

def run_baidu(kwd):
    """
    执行命令行运行函数
    获取百度搜索结果
    后台执行浏览器操作
    """
    # cmd_env="source activate;"
    output = './data/run_baidu'+str(time.time())+'.json'
    cmd='../bin/python3 bert_run_jianxie.py --do baidu --text """'+kwd+'""" --output '+output
    print(cmd)
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    print(data)
    return data
def run_cmd_url_text(url):
    """
    执行命令行运行函数
    获取网页内容
    """
    output = './data/url_text'+str(time.time())+'.json'
    cmd='../bin/python3 bert_run_jianxie.py --do url_text --url "'+url+'" --output '+output
    print(cmd)
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    
    return data

def run_cmd(cmd,inputfile,output):
    """
    执行命令行运行函数
    """
    # my_env = {**os.environ, 'PATH': '../bin/:/usr/sbin:/sbin:' + os.environ['PATH']}
    # subprocess.Popen(['source ','../bin/activate'],shell=True)
    e = subprocess.call(cmd, shell=True)


    # e = subprocess.Popen(cmd, shell=True,env=my_env).wait()

    # p = Popen("/path/to/env.sh", stdin=PIPE) # set environment, start new shell 
    # p.communicate("python something.py\nexit") # pass commands to the opened shell 
    # # e = subprocess.Popen([python_bin, script_file])
    # print(e)
    # e=os.system('. ../bin/activate &&'+cmd) 

    if e==0:
        print("执行成")
        # cmd_mv_corpu_list="mv "+item+" "+corpus_end_path
        with open(output,'r') as load_f:
            load_dict = json.load(load_f)
            # print(load_dict)
            os.remove(output)
            # os.remove(inputfile)
            return load_dict
    else:
        print("执行失败")
        return {'data':'','state':'fail'}



# text = "成年的腊肠犬体型也没多大"
# print(yuce(text))

