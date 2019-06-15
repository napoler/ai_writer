训练

>python gen_idf.py -i shuju -o idf.txt

# 生成idf
python3 gen_idf.py -i /home/terry/pan/github/ai_writer/ai_writer/data/kw2text/ -o idf.txt

python3 gen_idf.py -i /home/terry/pan/github/ai_writer/ai_writer/data/kw2text_mini/ -o ../../libs/idf.txt



python3 gen_idf.py -i /home/terry/pan/github/ai_writer/ai_writer/data/test/ -o ../../libs/idf.txt
python tfidf.py -i ../../libs/idf.txt -d t.txt -t 20