"""
将多个训练文件合并成为一个文件
已经进行分句处理


"""
# from libs import TerrySearch
# from .bert_run as run_cmd
# import bert_run
import configparser
import json,time,re
import Terry_toolkit as tkit
from tqdm import tqdm
corpus_path = '/home/terry/github/ai_writer/ai_writer/data/kw2text_mini/'
last = '../data/corpus_mini_v3.txt'
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



# text= ''
juzis_list =[]
for item in tqdm(tfile.file_List(corpus_path,'txt')):
    paragraph= openf(item)
    # 去除回车
    # paragraph= paragraph.strip('\n') 
    paragraph = tfile.clear(paragraph)
    new_sents = text2sentences(paragraph)
    if len(new_sents)>1:
        try:
            juzis = '\n'.join(new_sents)
            juzis_list.append(juzis)

            # text = text +'\n\n'+ '\n'.join(new_sents)
        except:
            pass
    else:
        print('内容过短')
    
text = '\n\n'.join(juzis_list)

my_open = open(last, 'a')
my_open.write(text)
my_open.close()



