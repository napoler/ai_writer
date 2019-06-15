import pynlpir
pynlpir.open()

s = '欢迎科研人员、技术工程师、企事业单位与个人参与NLPIR平台的建设工作。'
pynlpir.segment(s)


# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# import Terry_toolkit as tkit
# import pynlpir
# pynlpir.open()

# corpus_path = ''
# tfile=tkit.File()
# ttext=tkit.Text()

# #打开文件
# def openf(file):
#     tfile=tkit.File()
#     try:

#         text = tfile.open_file(file)
#         return  text
#     except:
#         pass

# def get_corpus(corpus_path):
 
#     for item in tfile.file_List(corpus_path,'txt'):
#         paragraph= openf(item)
#         return paragraph



# file='t.txt'
# s =openf(file)
# k= pynlpir.segment(s)
# print(k)
# # key_words = pynlpir.get_key_words(s, max_words=1000, weighted=True)
# # for key_word in key_words:
# #     print ('%s %s' % (key_word[0], int(key_word[1]*10)))