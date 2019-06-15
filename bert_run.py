from cacheout import Cache
cache = Cache()

#import multiprocessing as mp
from bert_sample import SentencePrediction,MaskedLM
import Terry_toolkit as tkit
import json,os
import argparse

import subprocess

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
    parser.add_argument('--model', type=str, default = None)
    # 需要加载的模型文件目录
    parser.add_argument('--do', type=str, default = None)
    # 需要执行的任务
    parser.add_argument('--output', type=str, default = './data/bert.json')
    # output 输出路径
    parser.add_argument('--input', type=str, default = None)
    # # --content 内容
    # parser.add_argument('--text', type=str, default=None)
    # # --text 前一句
    args = parser.parse_args()
    # print (args.content)
    # print (args.text)
    print (args.model)
    print (args.output)
    if args.do == 'Sentence_Pre':
        # 执行预测
        Sentence_Pre(args.model,args.output,args.input)
def Sentence_Pre(model,output,input):
    # 读取输入的文件
    with open(input,'r') as load_f:
        load_dict = json.load(load_f)
        # print(load_dict)

    nextS=SentencePrediction()
    nextS.model_init(model=model)
    text= load_dict['text']
    items = []
    for content in load_dict['content']:
    # content = load_dict['content']
        # print(content['content'])
        next_line=nextS.sentence(content['content'],text)
        # content['next_line'] =next_line
        # content['next_line'] =next_line
        items.append(next_line)

    with open(output,"w") as f:
        json.dump(items,f)
        print("推测结果保存在:"+output)
    #释放内存
    nextS.free_ram()
    return 





if __name__=='__main__':
    run()
#     model ='/home/terry/pan/github/bert/test/last/'
#     text = "如果在运行python脚本时需要传入一些参数"
#     content ="""
#     如果在运行python脚本时需要传入一些参数，例如gpus与batch_size，可以使用如下三种方式。

# python script.py 0,1,2 10
# python script.py -gpus=0,1,2 --batch-size=10
# python script.py -gpus=0,1,2 --batch_size=10
# 这三种格式对应不同的参数解析方式，分别为sys.argv, argparse, tf.app.run, 前两者是python自带的功能，后者是tensorflow提供的便捷方式。

# sys.argv
# sys模块是很常用的模块， 它封装了与python解释器相关的数据，例如sys.modules里面有已经加载了的所有模块信息，sys.path里面是PYTHONPATH的内容，而sys.argv则封装了传入的参数数据。 
# 使用sys.argv接收上面第一个命令中包含的参数方式如下：
    
    
#     """
#     Sentence_Pre(model,content,text)

