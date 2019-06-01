from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a",
                     content=u"柯基犬 就是 牛 This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b",
                     content=u"The second one is even more interesting!")
writer.commit()
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
     query = QueryParser("content", ix.schema).parse("柯基犬")
     results = searcher.search(query)
     if len(results)>0:
        print(results[0])
     print(results[0])


# from whoosh.query import *

# myquery = parser.parse(u"柯基犬 牛")
# # myquery = And([Term("content", u"柯基犬"), Term("content",u"牛")])

# results = searcher.search(myquery)
# print(len(results))
# print(results[0])