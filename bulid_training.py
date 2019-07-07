from fun import *
import json
import libs
import re
# output='/home/terry/pan/github/Bert-Sentence-streamlining/Bert-Sentence-streamlining/data/train_old.json'
# with open(output,'r') as f:
#     items=[]
#     for line in f:
#         j_content = json.loads(line)
#         if j_content['label']=="Yes":
#             items.append(j_content)
#             # add_sentence_one_unmark(j_content['sentence'])
#             add_sentence_one(j_content['sentence'])
#             # libs.Terry().c_inputfile('/home/terry/pan/github/Bert-Sentence-streamlining/Bert-Sentence-streamlining/data/train.json',j_content)
#     # load_dict = json.load(load_f)
#     print(len(items))
#     # libs.Terry().c_inputfile('/home/terry/pan/github/Bert-Sentence-streamlining/Bert-Sentence-streamlining/data/train_v3.json',items)



corpus='/home/terry/github/ai_writer/ai_writer/data/mark/corpus.txt'
with open(corpus,'r') as f:
    items=[]
    for line in f:
        # if j_content['label']=="Yes":
        p=re.compile(r'[##del##](.*?)[##del##]',re.S)
        words= re.findall(p, line)
        if len(words)>0:
            add_sentence_one(line)
        
 
