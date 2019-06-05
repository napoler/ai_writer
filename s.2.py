from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(title="救援 ( WildAid ) 举办 的 《 生机 无限", path="/a",
                     content="由 国际 环保 组织 野生 救援 ( WildAid ) 举办 的 《 生机 无限 》 周杰伦 保护 濒危 野生 生动 动物 野生动物 媒体 发布 发布会 在 京 召开 ， 知乎 作为 深度 科普 合作 伙伴 合作伙伴 出席 活动")
writer.add_document(title=u"Second document", path=u"/b",
                     content=u"The second one is even more interesting!")
writer.commit()

# 方法一 使用FileStorage对象
from whoosh.filedb.filestore import FileStorage
# storage = FileStorage('indexdir')  #idx_path 为索引路径
# ix = storage.open_index(indexname='indexdir', schema=schema)
from whoosh.index import open_dir
idx = open_dir(indexname='terry_search',dirname='indexdir')  #indexname 为索引名
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
     query = QueryParser("content", ix.schema).parse("濒危动物")
     results = searcher.search(query)
     if len(results)>0:
        print(results[0])
#      print(results[0])


# from whoosh.query import *

# myquery = parser.parse(u"柯基犬 牛")
# # myquery = And([Term("content", u"柯基犬"), Term("content",u"牛")])

# results = searcher.search(myquery)
# print(len(results))
# print(results[0])