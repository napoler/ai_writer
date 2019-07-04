# import os
# os.chdir("../")   #修改当前工作目录
# print(os.getcwd())    #获取当前工作目录
import libs

# import fun
extractor =libs.TripleExtractor()
content1 = """威尔士柯基犬（welsh corgi pembroke）是一种小型犬，但性格非常稳健，完全没有一般小型犬的神经质，是非常适合小孩的守护犬。它们的胆子很大，也相当机警，能高度警惕地守护家园，是最受欢迎的小型护卫犬之一。"""

svos = extractor.triples_main(content1)
print('svos', svos)
print('content1', content1)