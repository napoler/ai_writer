import libs
from tqdm import tqdm
import os
import shutil
import argparse

ARTICLE_PATH ="./data/wikitext/"
 
def run():
    """ 
    >>> python3 search2text.py --text 犬
    """
    parser = argparse.ArgumentParser(description='python3 search2text.py --text 犬')
    parser.add_argument('--text', type=str, default = None)
    #需要搜索的关键词

    args = parser.parse_args()

    text =args.text
    r= libs.TerrySearch().search(text=text,limit=1000000)
    # print(len(r))
    to =ARTICLE_PATH
    print('开始复制文件')
    for item in tqdm(r):
        # print(item['data']['path'])
        shutil.copy(item['data']['path'], to)

if __name__=='__main__':
    run()
