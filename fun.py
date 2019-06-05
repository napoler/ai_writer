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
