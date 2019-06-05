# from libs import TerrySearch
# from .bert_run as run_cmd
import bert_run
import configparser
import json,time
import Terry_toolkit as tkit
from tqdm import tqdm
corpus_path = '/home/terry/pan/github/ai_writer/ai_writer/data/book/'
item = 'data/corpus.txt'
tfile=tkit.File()


#打开文件
def openf(file):
    tfile=tkit.File()
    text = tfile.open_file(file)
    return  text


text =''
#   for num in range(0,50000):  # 迭代 10 到 20 之间的数字
#     f2 = choice(tfile.file_List(corpus_path,'txt'))
#     text = text + "\n\n"+ openf(f2)
for f2 in tqdm(tfile.file_List(corpus_path,'txt')):  # 迭代 10 到 20 之间的数字

    text = text + "\n\n"+ openf(f2)
my_open = open(item, 'a')
my_open.write(text)
my_open.close()


