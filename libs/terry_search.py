from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
class TerrySearch:
    """本地构建搜索
    """
    def __init__(self):
        """开始初始化搜索
        """
        pass
    def start(self,path):
        """开始执行搜索
        >>> start(path)
        """
        pass
    def add_one(self,one):
        
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        ix = create_in("indexdir", schema)
        writer = ix.writer()
        writer.add_document(title=u"First document", path=u"/a",
                            content=u"柯基犬 就是 牛 This is the first document we've added!")
        writer.add_document(title=u"Second document", path=u"/b",
                            content=u"The second one is even more interesting!")
        writer.commit()
