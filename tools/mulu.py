"""
防止单个目录文件过多
"""
import Terry_toolkit as tkit
# import xrange
tfile=tkit.File()
ttext=tkit.Text()
corpus_path = '/home/terry/pan/github/ai_writer/ai_writer/data/book/'

import os,time
import shutil
# def mkdir(path):
 
# 	folder = os.path.exists(path)
 
# 	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
# 		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
# 		print ("---  new folder...  ---")
# 		print ("---  OK  ---")
 
# 	else:
# 		print ('---  There is this folder!  ---')
 

path ='/home/terry/pan/github/ai_writer/ai_writer/data/book_fast/'
tfile.mkdir(path)
do_path_one = path+str(time.time())+'/'
tfile.mkdir(do_path_one)

i = 0
for item in tfile.file_List(corpus_path,'txt'):
    # print(key)
    print(item)
    

    if i%5000 ==0:
         # 创建一层目录
        if len(os.listdir(do_path_one))<1000:
            pass
        # elif len(os.listdir(do_path_one))==1000:
        #     do_path_one = path+str(time.time())+'/'
        else:
            do_path_one = path+str(time.time())+'/'
            tfile.mkdir(do_path_one)

        # 创建二层目录
        do_path= do_path_one+str(time.time())
        # do_path= path+str(time.time())
        tfile.mkdir(do_path)
    #执行复制
    shutil.copy(item, do_path)
    # if(os.listdir(path))
    i =i+1
