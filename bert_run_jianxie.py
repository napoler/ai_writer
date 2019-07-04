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

def prediction(text):
    """
    执行命令行运行函数
    这里是简化
    """
    cmd="python3 bert_run_jianxie.py --text "+text
    output = './data/jianxie.json'
    inputfile=''
    data = run_cmd(cmd,inputfile,output)
    return data


def run_cmd(cmd,inputfile,output):
    """
    执行命令行运行函数
    """
    e = subprocess.call(cmd, shell=True)
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
    parser.add_argument('--do', type=str, default = 'jianxie')
    # 需要执行的任务
    parser.add_argument('--output', type=str, default = './data/jianxie.json')
    # output 输出路径
    parser.add_argument('--text', type=str, default = None)
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


        # print()
        print(t)
        r= word_list[i]
        if t[0]==0 :
            print('\n删除:'+word_list[i])
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

