# encoding=utf-8
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
import jieba
from jieba.analyse import ChineseAnalyzer
from tqdm import tqdm
# indexname
# INDEXNAME='TerrySearch'
INDEXNAME='TerrySearch_pet'
# from Terry_toolkit import File
import Terry_toolkit
class TerrySearch:
    """本地构建搜索
    """
    def __init__(self):
        """开始初始化搜索
        """
        pass
    def init_search(self):
        """初始化搜索

        """
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        # ix = create_in("indexdir", schema)
        idx = create_in("indexdir", schema=schema, indexname=INDEXNAME) #path 为索引创建的地址，indexname为索引名称  

    def start(self,path=''):
        """开始执行搜索
        >>> start(path)
        """
        # schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        # ix = create_in("indexdir", schema)

        #打开搜索
        idx = open_dir("indexdir", indexname=INDEXNAME)  #读取建立好的索引  
        writer = idx.writer()

        #https://terry-toolkit.terrychan.org/zh/master/Terry_toolkit.file/#Terry_toolkit.file.File.file_List
        i =0
        flist= Terry_toolkit.File().file_List(path=path, type='txt')
        print('文件数目')
        print(len(flist))
        for item in tqdm(flist):
            # print('item:  '+item)
            try:
                text = Terry_toolkit.File().open_file(item)

                
                # seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
                # # print(", ".join(seg_list))
                # text_fenci=" ".join(seg_list)
                # print(text_fenci)
                # print("标题:"+text[0:30])
                writer.add_document(title=text[0:30] , path=item,
                                    content=text)
                if i%10000 == 0:
                    #每10000次提交一次
                    writer.commit()
                    writer = idx.writer()
            except:
                pass
                
            i =i +1

            
        writer.commit()
        pass
    def search(self,text='',limit=10):
        """搜索内容 自动分词
        >>> search(text)
        """
        seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
        # print(", ".join(seg_list))
        text=" ".join(seg_list)
        results =  self.search_keyword(keyword= text,limit=limit)

        # print(results[0])
        # for i in range(0,len(results)):
        #     print(i)
        #     print(results[i])

        #     items.append(results[i])
        # return items

        # print(results)
        return results
        # print(results[0])
   
 

    def search_keyword(self,keyword='',limit=10):
        """搜索内容
        >>> search(keyword)
        """
        #打开搜索
        idx = open_dir("indexdir", indexname=INDEXNAME)  #读取建立好的索引  
        # writer = idx.writer()
        with idx.searcher() as searcher:
            print('搜索关键词:'+keyword)
            # results =
            query = QueryParser("content", idx.schema).parse(keyword)
            try:
                
                results = searcher.search(query,limit=limit)
                # print(results)
                # return results
            except:
                return 
            items =[]
            # for item in results:
            #     print(item.Hit['title'])  
            for hit in results:
                # 着重显示
                # print(hit.highlights("content"))
                # print(hit.highlights("title"))
                # print(dict(hit))
                data = {
                    'data':dict(hit),
                    'highlights':hit.highlights("content")
                }
                items.append(data)
            return items

            #     print(dict(item))  
            #     items.append(dict(item))
            # return items
            # finally:
            #     searcher.close()
                

            # print(len(results))
            # if len(results)>0:
            #     print(results[0])
            # print(results[0])
            
 
 

    # def add_item(self,item):
        
    #     schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    #     ix = create_in("indexdir", schema)
    #     writer = ix.writer()
    #     writer.add_document(title=u"First document", path=u"/a",
    #                         content=u"柯基犬 就是 牛 This is the first document we've added!")
    #     writer.add_document(title=u"Second document", path=u"/b",
    #                         content=u"The second one is even more interesting!")
    #     writer.commit()
