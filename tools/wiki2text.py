# from libs import TerrySearch
# import src
import Terry_toolkit as tkit
import time
import random
import csv
import os
from random import choice
import hashlib
import json
from tqdm import tqdm
ARTICLE_PATH ="../data/wiki/"
PATH ="/media/terry/65F33762C14D581B/tdata/wiki_zh/"

def run():
        tfile = tkit.File()
        path =PATH
        file_list = tfile.all_path(path)
        # print(file_list)
        for file in tqdm(file_list):
                # print(file)
                for line in open(file): 
                        json_line=json.loads(line)
                        # print (json_line) 
                        # print (json_line['text']) 
                        save_article(json_line['text'])


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
 
if __name__=='__main__':
        run()