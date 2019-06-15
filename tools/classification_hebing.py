"""
构建bert分类训练需要的数据
"""

# from libs import TerrySearch
# from .bert_run as run_cmd
# import bert_run
import configparser
import json,time,re
import Terry_toolkit as tkit
from tqdm import tqdm
import random
import hashlib


# #宠物数据
corpus_path_1 = '/home/terry/pan/github/ai_writer/ai_writer/data/kw2text_mini/' #
#其他数据
corpus_path_2 = '/home/terry/github/ai_writer/ai_writer/data/kw2text_other/'

# 创建dev数据


last = '../data/train.json'
last_1 = '../data/train1.json'
dev = '../data/dev.json'
# item = 'data/article_30e0446c6d5915a10c4a939d70dff353.txt'

tfile=tkit.File()
ttext=tkit.Text()

#打开文件
def openf(file):
    tfile=tkit.File()
    try:

        text = tfile.open_file(file)
        return  text
    except:
        pass


def text2sentences(paragraph):
    """分句函数
    """
    # pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    # pattern ='(。|！|\!|\.|？|\?|\,|，|\;|；|\:|)'
    # pattern ='(。|！|\!|\.|？|\?|\;|；)'
    pattern ='(。|！|\!|？|\?|\;|；)'
    sentences = re.split(pattern,paragraph)         # 保留分割符
    

    new_sents = []
    for i in range(int(len(sentences)/2)):
        sent = sentences[2*i] + sentences[2*i+1]
        new_sents.append(sent)
    return new_sents

# new_sents = text2sentences(paragraph)

def c_inputfile(inputfile,data):
    """创建预测文件

    """
    with open(inputfile,"w") as f:
        json.dump(data,f)
        print("创建训练资料完成..."+inputfile)
        return True

# text= ''
def creat_corpus(corpus_path,lei):
    juzis_list =[]
    print(len(tfile.file_List(corpus_path,'txt')))
    i = 0
    for item in tqdm(tfile.file_List(corpus_path,'txt')):
        paragraph= openf(item)
        # 去除回车
        # paragraph= paragraph.strip('\n') 
        paragraph = tfile.clear(paragraph)
        new_sents = text2sentences(paragraph)
        item_md5 = hashlib.md5(str(paragraph).encode('utf8')).hexdigest()
        
        if len(new_sents)>0:
            for j in new_sents:
                juzis={
                    'label':lei,
                    'sentence':j,
                    'text_hash':item_md5

                }
                juzis_list.append(juzis)
                i = i+1
        else:
            # print('内容过短')
            # print(new_sents)
            # print(paragraph)
            pass
        
    # text = ''.join(juzis_list)
    print(len(juzis_list))
    print('句子为:')
    print(i)
    # print(juzis_list)
    return juzis_list


# 开始运行
lei='1'
text1= creat_corpus(corpus_path_1,lei)
lei='0'
text2= creat_corpus(corpus_path_2,lei)
text = text1+text2
# print(len(text))
# c_inputfile(last_1,text)

random.shuffle(text)

c_inputfile(last,text)
# len()
dev_text = random.sample(text, 500)  #从list中随机获取5个元素，作为一个片断返回  
# print (slice) 
c_inputfile(dev,dev_text)

# my_open = open(last, 'a')
# my_open.write(text)
# my_open.close()



