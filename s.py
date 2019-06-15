# from libs import TerrySearch
# from libs import TerrySearch
import libs
import fun
# import tqbm
 

def get_keywords(text):
    kw = libs.Keyword(topK=5,allowPOS= ('ns', 'n', 'vn', 'v','t')  )
    kws= kw.get_keyword_list(text)
    return kws
 
text= "母犬孕期喂养要精心，饲料营养要丰富，数量要充足，任其自由取食。投喂众所周知的，葡萄洋葱巧克力生鸡蛋都是柯基犬的天敌，不仅是柯基犬，所有品种的**狗狗**绝对不能喂，这种一旦吃上，就会威胁到柯基的血液之中，严重的时候可能有生命危险 "
k  =get_keywords (text)
print(k)


kw = libs.Keyword()
kws= kw.get_keyword_pseg(text)
print(kws)