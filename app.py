from cacheout import Cache
cache = Cache()
import torch
from flask import Flask, render_template, request, json, Response, jsonify
import gc,time
from sys import getrefcount
import resource
from functools import partial
import libs
#同义词
import synonyms
import bert_run
#import multiprocessing as mp
from bert_sample import SentencePrediction,MaskedLM
import Terry_toolkit as tkit
import configparser
from fun import *

config = configparser.ConfigParser()

config.read("./config/config.ini")

# config.get('site', 'user'))
app = Flask(__name__)


@app.route("/")
def home():
    print(config.get('site', 'name'))
    return render_template("index.html")


@app.route("/post/list")
def post_list():
    print(config.get('site', 'name'))
    # id_list
    tfile =  tkit.File()
    id_list=tfile.file_List('./data/article/')
    new_id_list  =[]
    for item in id_list:
        id=item.split("/")[-1]
        
        new_id_list.append(id.replace(".txt", ""))
    #降序输出
    print(new_id_list.sort(reverse=True))
    return render_template("post_list.html",id_list=new_id_list)
@app.route("/json/save/post", methods=['GET', 'POST'])
def json_save_post():
    """
    保存内容
    输入id
    和text

    """
    data= get_post_data()
    # print('data',data)
    text = data['text']
    id =  data['id']

    save_article_plus(text,id)
    d={'state':True
    }
    
    return jsonify(d)


@app.route("/json/auto_sort", methods=['GET', 'POST'])
def json_auto_sort():
    """
    进行文章排序

    """
    data= get_post_data()
    print('data',data)
    text = data['text']
    aid = data['aid']
    run_auto_sort(text,aid)
    d={'state':True
    }
    
    return jsonify(d)





@app.route("/json/get/post", methods=['GET', 'POST'])
def json_get_post():
    """
    获取内容
    输入id
    和text

    """
    data= get_post_data()
    # print('data',data)
    # text = data['text']
    id =  data['id']
    text_list=get_article_plus(id)
    d={'state':True,
        'data':text_list
    }
    print(d)
    return jsonify(d)
@app.route("/json/nlp", methods=['GET', 'POST'])
def json_nlp():
    text = request.args.get('text')
    print('text:',text)

    key ='page_nlp'+str(text)
    if cache.get(key) is None:
        print('创建新缓存')

        tnlp = libs.Nlp()
        keywords = tnlp.dnn(text=text)
        cache.set(key ,keywords)
    else:
        print('获取缓存')
        keywords = cache.get(key)
    print('dnn:',keywords)
    return jsonify(keywords)
@app.route("/json/calculate_keyword", methods=['GET', 'POST'])
# 获取关键词
def json_calculate_keyword():
    text = request.args.get('text')
    cache_key ='json_calculate_keyword'+str(text)
    if cache.get(cache_key) is None:
        # 抽取名称和形容词
        # synonyms
        # kws,s = synonyms.seg(text)
        # # kws =tkit.Text().get_keywords(text,num=3)
        # l = {'n','nz','ns','nr'}
        # # kws_new = []
        # keyword =''
        # for key,item in enumerate(s):
        #     print(key)
        #     print(item)

        #     print(kws[key])
        #     if item in l:
        #         keyword = keyword+" "+kws[key]
        
        # keywords = tkit.Text().get_keywords( text,num=4)
        keywords =get_keywords(text)
        data= ' '.join(keywords)
        # data= ''
        # for item in keywords:
        #     # data = data +' '+ item['word']
        #     data = data +' '+ item

        cache.set(cache_key ,data)
    else:
        print('获取缓存')
        data = cache.get(cache_key)
    # print('dnn:',data)
    return jsonify(data)   


def get_keywords(text):
    """获取关键词

    """
    kw = libs.Keyword(topK=3,allowPOS= ('ns', 'n', 'vn', 'v','t'))
    kws= kw.get_keyword_list(text)
    return kws


@app.route("/json/calculate", methods=['GET', 'POST'])
# 预测下一句
def json_calculate():
    text = request.args.get('text')
    print('text:',text)
    if request.args.get('keyword'):

        keyword = request.args.get('keyword')
    else:
        keyword = get_keywords(text)
        keyword= ' '.join(keyword)
        # keywords = tkit.Text().get_keywords( text,num=4)
        # data= ''
        # for item in keywords:
        #     keyword = data +' '+ item['word']

    print(keyword)

    cache_key ='json_calculate'+str(text)+str(keyword)
    if cache.get(cache_key) is None:
        print('创建新缓存')

        # tnlp = libs.Nlp()
        # keywords = tnlp.dnn(text=text)
        # items,items_rank = synonyms.nearby(text)
        items= libs.TerrySearch().search(text=keyword,limit= int(10))
        # nextS=SentencePrediction()
        mod= config.get('bert', 'model')
        # nextS.model_init(model=mod)
        nexts = []
        next_lines=[]
        contents=[]
        if len(items)==0:
            msg ='搜索内容为空'
            data = {

                    'msg':msg
                }
            # cache.set(cache_key ,data)
        else:
        
            for item in items:
                # print(item['data'])
                article = tkit.Text().text_processing(item['data']['content'],5)

                # items.append(text)
                # nextS.model_init()
        
                
                # article ={
                #     'calculate':next_line,
                #     'content':item
                # }

                nexts.append(article)
                # contents.append(item['data']['content'])
                contents.append(item['data'])

            pdata = {
                'content':contents,
                'text':text
            }
            tmpname = str(time.time())
            output ='/tmp/output_'+tmpname+'.json'
            inputfile ='/tmp/input_'+tmpname+'.json'
            bert_run.c_inputfile(inputfile,pdata)
            # torch.cuda.empty_cache()
            try:
                # next_line=nextS.sentence(item['data']['content'],text)


                # if bert_run.c_inputfile(inputfile,pdata):
                print('开始后台执行')
                cmd ="python3 bert_run.py --model "+mod+" --do Sentence_Pre --output "+output+ " --input "+inputfile
                next_lines = bert_run.run_cmd(cmd,inputfile,output)

                # article['calculate'] = next_line
                # next_lines = next_lines+next_line
                # else:
                #     print('创建训练文件出错')
                
            except:
                # next_line=[]
                print("运行预测失败")
                msg ='预测失败'
                # torch.cuda.empty_cache()
                pass
                #排序所有句子
            msg ='预测成功 文章'+str(len(items))
            full_next_line=[]
            for  next_line in next_lines:
                full_next_line =full_next_line +next_line
            # full_next_line=list(set(full_next_line))
            news_ids = []
            for id in full_next_line:
                if id not in news_ids:
                    news_ids.append(id)
            next_lines = sorted(news_ids, key=lambda k: k['next_line_prediction'],reverse=True)
            next_lines_top= next_lines[0:9]
            

            data = {
                'next_lines_top':next_lines_top,
                'article':nexts,
                'text':text,
                'keyword':keyword,
                'msg':msg
            }

        cache.set(cache_key ,data)
    else:
        print('获取缓存')
        data = cache.get(cache_key)
    # print('dnn:',data)
    return jsonify(data)
# 获取相关词
@app.route("/json/synonyms", methods=['GET', 'POST'])
def json_synonyms():
    text = request.args.get('text')
    print('text:',text)

    key ='json_synonyms'+str(text)
    if cache.get(key) is None:
        print('创建新缓存')

        # tnlp = libs.Nlp()
        # keywords = tnlp.dnn(text=text)
        items,items_rank = synonyms.nearby(text)
        cache.set(key ,items)
    else:
        print('获取缓存')
        items = cache.get(key)
    print('dnn:',items)
    return jsonify(items)

# 伪原创语句
@app.route("/json/rewrit/statement", methods=['GET', 'POST'])
def json_rewrit_statement():
    text = request.args.get('text')
    print('text:',text)

    key ='json_rewrit_statement'+str(text)
    if cache.get(key) is None:
        print('创建新缓存')

        # tnlp = libs.Nlp()
        # keywords = tnlp.dnn(text=text)
        rs = libs.RewritStatement()
        # text ="python中for循环输出列表索引与对应的值 - tanlangqie的博客"
        t = rs.text(text)
        rnk = synonyms.compare(text, t, seg=True)
        items = {
            'text':text,
            'new_text':t,
            'relevant':rnk
        }
        # print(t)
        cache.set(key ,items)
    else:
        print('获取缓存')
        items = cache.get(key)
    print('json_rewrit_statement',items)
    return jsonify(items)

@app.route("/json/get_url" ,methods=['GET', 'POST'])
def json_get_url():
    """返回搜索json结果
    """
    url = request.args.get('url')

    key ='json_get_url'+url
    if cache.get(key) is None:
        # data=url_text(url)
        data=run_cmd_url_text(url)
        
        
        if data['state']=='success':
            r = tkit.Text().text_processing(data['data'], num=5)
        # print(data)
        
            data={'data':r,
                'msg':'返回数据'
            }
        else:
            data={'data':'',
                'msg':'获取失败'
            }
        
        cache.set(key ,data)
    # data 
    else:
        print('获取缓存')
        data = cache.get(key)
    return jsonify(data)

@app.route("/json/search_baidu" ,methods=['GET', 'POST'])
def json_search_baidu():
    """返回搜索json结果
    """
    keyword = request.args.get('keyword')
    
    key ='json_search_baidu'+keyword
    if cache.get(key) is None:
        # data=url_text(url)
        # data=run_cmd_url_text(url)
        
        
        r = baidu_search(keyword)
        # print(r)
    
        data={'data':r,
            'msg':'返回数据'
        }
       
        
        cache.set(key ,data)
    # data 
    else:
        print('获取缓存')
        data = cache.get(key)
    return jsonify(data)



@app.route("/json/search" ,methods=['GET', 'POST'])
def json_search():
    """返回搜索json结果
    """
    text = request.args.get('text')
    limit = request.args.get('limit')
    print(limit)
    r= libs.TerrySearch().search(text=text,limit= int(limit))
    # print(data)
    # data={'data':r,
    #     'msg':'返回数据'
    # }
    # data 
    return jsonify(r)



@app.route("/json/search_pre" ,methods=['GET', 'POST'])
def json_search_pre():
    """返回搜索json结果 并且进行预处理
    """
    text = request.args.get('text')
    limit = request.args.get('limit')

    key ='json_search_pre'+text+str(limit)
    if cache.get(key) is None:
    # print(limit)
        r= libs.TerrySearch().search(text=text,limit= int(limit))
        items = []
        for item in r:
            item['data']['content']
            print(item['data']['content'])
            # tkit.Text().get_keyphrases(item['data']['content'], num=10)
            text = tkit.Text().text_processing(item['data']['content'], num=5)
            items.append(text)
        cache.set(key ,items)
    else:
        print('获取缓存')
        items = cache.get(key)
    return jsonify(items)

# 编辑器页面
@app.route("/p/edit")
def page_edit():
    # keyword = request.args.get('keyword')
    # num = request.args.get('num')
    # key ='page_Summary_by_keywords'+keyword+str(num)
    key ='p_edit'

    if cache.get(key) is None:
        print('创建新缓存')
        # zy = Summarynew.Summary()
        # content = zy.search(keyword=keyword,num=int(num))
        content = []
        cache.set(key ,content)
    else:
        print('获取缓存')
        content = cache.get(key)
    print(content)
    return render_template("edit_v1.html",**locals())
@app.route("/tools/sentence/prediction")
def tools_sentence_prediction():
    return render_template("tools_sentence_prediction.html",**locals())

@app.route("/json/sentence/prediction" ,methods=['GET', 'POST'])
def json_sentence_prediction():
    data= get_post_data()
    print('data',data)
    # paragraph = request.args.get('text')
    # previous_line=request.args.get('sentence')
    paragraph = data['text']
    previous_line = data['sentence']
    print('paragraph',paragraph)
    print('previous_line',previous_line)

    if paragraph and previous_line:
        nextS=SentencePrediction()
        mod= config.get('bert', 'model')
        nextS.model_init(model=mod)
        # nextS.model_init()
        next_line=nextS.sentence(paragraph,previous_line)

        #释放内存
        nextS.free_ram()
        del nextS
        gc.collect()
        # print(len(next_line))
        # print('next_line',next_line[:10])
        # data=next_line[:10].tolist()
        data={'data':next_line}

        data['msg']='返回预测结果'
    else:
        data={'msg':'数据不完整'}
    return jsonify(data)
    # return "Hello World!"
@app.route("/json/sentence/fenci")
def json_sentence_fenci():
    """
    获取分词 预测
    
    """
    text = request.args.get('text')
    seg_list=yuce(text)
    data={
        'seg_list':seg_list,
        'text':text

    }
    return jsonify(data)



@app.route("/json/fenci_update")

def json_sentence_fenci_update():
    """
    执行提交后处理提交
    """
    # data= get_post_data()
    # print('data',data)
    text1 = request.args.get('text1')
    text2 = request.args.get('text2')
    # previous_line=request.args.get('sentence')
    # text = data['text']
    # text2 = data['text2']
    # seg_list=[]
    # for it in jieba.cut(text, cut_all=False):
    # # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    # # print()
    #     seg_list.append(it)



    #保存词性训练数据
    # libs_text= libs.Text()
    text1_pseg  =libs.Text().text_part_pseg(text1)
    text2_pseg  =libs.Text().text_part_pseg(text2)
    file_pseg_write_obj = open("./data/mark/corpus_pseg.txt", 'a')
    #python2可以用file替代open
    # for var in mylist:
    text_pseg = text1_pseg+"\n"+text2_pseg+"\n\n"
    file_pseg_write_obj.writelines(text_pseg)
    file_pseg_write_obj.close()


    #保存训练数据
    file_write_obj = open("./data/mark/corpus.txt", 'a')
    #python2可以用file替代open
    # for var in mylist:
    text = text1+"\n"+text2+"\n\n"
    file_write_obj.writelines(text)

    # 创建bert使用的训练数据
    # #随机产生一条
    # random_sentence_one()


        #先写入columns_name
        # writer.writerow(["index","a_name","b_name"])
        #写入多行用writerows
        # writer.writerows([[text1,text2]])

    file_write_obj.close()

    # 添加一条标记数据
    add_sentence_one(text2)
    return jsonify('')







@app.route("/json/move_used")

def json_move_used():
    """
    执行提交后处理提交
    """
    # data= get_post_data()
    # print('data',data)
    id = request.args.get('id')
    move_used(id)

    return jsonify('')







@app.route("/tools/sentence/gaicuo")
def tools_sentence_gaicuo():
    return render_template("tools_sentence_gaicuo.html",**locals())

#改错
@app.route("/json/sentence/gaicuo" ,methods=['GET', 'POST'])
def json_sentence_gaicuo():
    data= get_post_data()
    print('data',data)
    # paragraph = request.args.get('text')
    # previous_line=request.args.get('sentence')
    text1 = data['text1']
    text2 = data['text2']
    # print('paragraph',paragraph)
    # print('previous_line',previous_line)

    if text1 and text2:

        text_new,text_new1=mlm(text1,text2)
        # p = mp.Pool(1)
        # prod_x=partial(mlm, text2=text2) # prod_x has only one argument x (y is fixed to 10)
        # text_new,text_new1 = p.map(prod_x,text1)
        # print rslt
#         print(getrefcount(mlm))
        # print(len(next_line))
        # print('next_line',next_line[:10])
        # data=next_line[:10].tolist()

        data={'data':{
            'text_new':text_new,
            'text_new1':text_new1

        }

        }

        data['msg']='返回预测结果'
    else:
        data={'msg':'数据不完整'}

    gc.collect()
    return jsonify(data)
    # return "Hello World!"

def mlm(text1,text2):
    print(text1,text2)
 
    # nextS=SentencePrediction()
    # next_line=nextS.sentence(paragraph,previous_line)
    mlm=MaskedLM()
    #初始化模型
    mod= config.get('bert', 'model')
    mlm.model_init(model=mod)
    # text1="今天天气好吗 "
    # text2="估计n牛错。"
    indexed_tokens,segments_ids= mlm.sentence_pre(text1,text2)

    # print(t)
    text_new,text_new1=mlm.prediction(indexed_tokens,segments_ids)
    #释放内存
#         mlm.free_ram()
    print('getrefcount(mlm)',getrefcount(mlm))
    #释放显存
    # mlm.clear()
    # # mlm.free_ram()
 
    del mlm
    gc.collect()

    return text_new,text_new1




if __name__ == "__main__":
    # app.run()
    app.run(
        host='0.0.0.0',
        port=9001,
        debug=True)