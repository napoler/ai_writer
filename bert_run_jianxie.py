#!/home/terry/pan/github/ai_writer/bin/python3

from cacheout import Cache
cache = Cache()

#import multiprocessing as mp
from bert_sample import SentencePrediction,MaskedLM
import Terry_toolkit as tkit
import json,os
import argparse
from flask import Flask, render_template, request, json, Response, jsonify
import jieba
import sqlite3
import csv,re
import libs
from random import choice
import random
import gc
import subprocess
from fun import *
import configparser
config = configparser.ConfigParser()

config.read("./config/config.ini")

def prediction(text):
    """
    执行命令行运行函数
    这里是简化
    """
    output = './data/jianxie'+str(time.time())+'.json'
    cmd="../bin/python3 bert_run_jianxie.py --do jianxie --output "+output+" --text "+text
    print(cmd)
    # cmd="python3 bert_run_jianxie.py --text "+text
    # output = './data/jianxie.json'
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    return data



def run_cmd_url_text(url):
    """
    执行命令行运行函数
    这里是简化
    """
    output = './data/url_text'+str(time.time())+'.json'
    cmd="../bin/python3 bert_run_jianxie.py --do url_text --url "+url+' --output '+output
    
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    return data

def run_baidu_cmd(kwd):
    """
    执行命令行运行函数
    这里是简化
    """
    output = './data/url_text'+str(time.time())+'.json'
    cmd=["../bin/python3", "bert_run_jianxie.py --do baidu --text "+kwd+' --output '+output]
    
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    return data


def run_cmd(cmd,inputfile,output):
    """
    执行命令行运行函数
    """
    # e = subprocess.call(cmd, shell=True)
    e = subprocess.Popen(cmd, shell=True)
    print(e)

    if e==0:
        print("执行成")
        # cmd_mv_corpu_list="mv "+item+" "+corpus_end_path
        with open(output,'r') as load_f:
            load_dict = json.load(load_f)
            # print(load_dict)
            os.remove(output)
            os.remove(inputfile)
            return load_dict
def c_inputfile(inputfile,data):
    """创建预测文件

    """
    with open(inputfile,"w") as f:
        json.dump(data,f)
        print("创建训练资料完成..."+inputfile)
        return True

def run ():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--model', type=str, default = '/mnt/data/dev/model/bert-rewrite-sentences/')
    # 需要加载的模型文件目录
    parser.add_argument('--do', type=str, default = None)
    # 需要执行的任务
    parser.add_argument('--output', type=str, default = None)
    # output 输出路径
    parser.add_argument('--text', type=str, default = None)

    parser.add_argument('--id', type=str, default = None)

    parser.add_argument('--url', type=str, default = None)
    # # --content 内容
    # parser.add_argument('--text', type=str, default=None)
    # # --text 前一句
    args = parser.parse_args()
    # print (args.content)
    # print (args.text)
    print (args.model)
    print (args.output)
    if args.do == 'jianxie':
        # 执行预测
        jianxie(args.model,args.output,args.text)
    if args.do == 'url_text':
        # 执行预测
        run_url_text(args.output,args.url)

    if args.do == 'baidu':
        # 执行预测

        run_baidu(args.output,args.text)

    if args.do == 'auto_sort':
        # 执行预测

        auto_sort(args.text,args.id)
def auto_sort(text,id):
    nextS=SentencePrediction()
    mod= config.get('bert', 'model')
    nextS.model_init(model=mod)
    t_text=tkit.Text()
    text_list=t_text.sentence_segmentation(text)
    print(text_list)
    text_list_mini=t_text.sentence_segmentation(text)
    # new_text='。'.join(text_list_mini)
    # print('new_text',new_text)
    l=[]
    #随机获取第一句
    # next_s=random.choice(text_list)
    # 第一句固定
    next_s=text_list[0]
    Article=next_s
    print('文章开始:+++++++++++++')
    for i in range(0,len(text_list)):
        # print(line)
        print(next_s)

        if len(text_list_mini)>1:
            text_list_mini.remove(next_s)
            new_text='。'.join(text_list_mini)
            # print('new_text',new_text)
            next_line=nextS.sentence(new_text,next_s)
            # print(next_line)
            if len(next_line)>0:
                next_s=next_line[0]['line_to_check']
                # print(next_s)
                # l.append(next_line[0])
                Article=Article+'。'+next_s

        elif len(text_list_mini)==1:
            Article=Article+'。'+text_list_mini[0]+'。'
            break

            # l.append(next_line[0])
    # print(l)
    # data ={
    #     'start':next_s
    #     'next':sentence
    # }
    # print(Article)
    save_article_plus(Article,id)
    return 
    pass


def run_baidu(output,keyword):
    print("已经运行来")
    # data= url_text(url)
    bsearch = libs.BaiduSearch()
    data,kws = bsearch.search(keyword=keyword,num = 0)
    print(data,kws)
    with open(output,"w") as f:
        json.dump(data,f)
        print("保存获取url内容到:"+output)
    return
def run_url_text(output,url):
    print("已经运行来")
    print("保存获取url内容到:"+output)
    data= url_text(url)

    with open(output,"w") as f:
        json.dump(data,f)
        
    return


def jianxie(model,output,text):
    # model =""
    cf= libs.Classifier(model)

    text_list,word_list = c_list(text)
    print(text_list)
    # word_list=jieba_seg_list(text)
    print(word_list)
    new_word=[]
    data=[]
    for i,item in enumerate(text_list):

        # print(item)

        t =cf.prediction(item)
        print('\n删除:'+word_list[i],t[0])

        # print()
        # print('t',t)
        r= word_list[i]
        if t[0]==0 :
            # print('\n删除:'+word_list[i],t[0])
            # while r in word_list:
            #     word_list.remove(r)
            word ={
                'word':word_list[i],
                'remove':"Yes"

            }
        else:
            new_word.append(word_list[i])
            word ={
                'word':word_list[i],
                'remove':"No"

            }
        data.append(word)
    print(data)
    with open(output,"w") as f:
        json.dump(data,f)
        print("推测结果保存在:"+output)
    # libs.Terry().c_inputfile('data/jianxie.json',data)

    # nextS=SentencePrediction()
    # nextS.model_init(model=model)
    # text= load_dict['text']
    # items = []
    # for content in load_dict['content']:
    # # content = load_dict['content']
    #     # print(content['content'])
    #     next_line=nextS.sentence(content['content'],text)
    #     # content['next_line'] =next_line
    #     # content['next_line'] =next_line
    #     items.append(next_line)

    # with open(output,"w") as f:
    #     json.dump(items,f)
    #     print("推测结果保存在:"+output)
    # #释放内存
    # nextS.free_ram()
    return 





if __name__=='__main__':
    run()

