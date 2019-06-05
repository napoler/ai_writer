# from libs import TerrySearch
# from .bert_run as run_cmd
# import bert_run
import configparser
import json,time,re
import Terry_toolkit as tkit
from tqdm import tqdm
corpus_path = '/home/terry/pan/github/ai_writer/ai_writer/data/book/'
item_or = 'data/corpus.txt'
item_new = 'data/corpus_new.txt'
# item = 'data/article_30e0446c6d5915a10c4a939d70dff353.txt'

tfile=tkit.File()
ttext=tkit.Text()

#打开文件
def openf(file):
    tfile=tkit.File()
    text = tfile.open_file(file)
    return  text

paragraph =  openf(item_or)


# juzi = re.split('(。|！|\!|\.|？|\?|\：|\:|\?)',text)
# juzi = ttext.sentence_segmentation(text)
# print(juzi)
def text2par(paragraph):
    """分段落函数
    """
    sentences = re.split('\n\n',paragraph)         # 保留分割符
    new_list =[]
    for it in sentences:
        new_list.append(it.replace("\n",""))
    return new_list


def text2sentences(paragraph):
    """分句函数
    """
    sentences = re.split('(。|！|\!|\.|？|\?)',paragraph)         # 保留分割符

    new_sents = []
    for i in range(int(len(sentences)/2)):
        sent = sentences[2*i] + sentences[2*i+1]
        new_sents.append(sent)
    return new_sents

new_sents = text2par(paragraph)
# print(new_sents)

all_sents =[]
for item in new_sents:
 
    sentences_list=text2sentences(item)
    if len(sentences_list)>1:
        all_sents.append('\n'.join(sentences_list))
# print(all_sents)
juzis=''

# for j in tqdm(new_sents):
#     juzis = juzis + "\n"+ j
juzis = '\n\n'.join(all_sents)
my_open = open(item_new, 'a')
my_open.write(juzis)
my_open.close()


# for f2 in tqdm(tfile.file_List(corpus_path,'txt')):  # 迭代 10 到 20 之间的数字

#     text = text + "\n\n"+ openf(f2)
# my_open = open(item, 'a')
# my_open.write(text)
# my_open.close()


