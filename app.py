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

config = configparser.ConfigParser()

config.read("./config.ini")

# config.get('site', 'user'))
app = Flask(__name__)


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
@app.route("/")
def home():
    print(config.get('site', 'name'))
    return render_template("index.html")

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
            text = tkit.Text().text_processing(item['data']['content'])
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
    app.run()
    # app.run(
    #     host='0.0.0.0',
    #     port=8110,
    #     debug=True)