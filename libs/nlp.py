# -*- coding: utf-8 -*-
from aip import AipNlp
import configparser

config = configparser.ConfigParser()

config.read("./config/config.ini")


class Nlp:

    # empCount = 0

    def __init__(self):
        print('kaishi')
        # self.text = text
        # self.salary = salary
        # Employee.empCount += 1

        # """ 你的 APPID AK SK """

    def dnn(self, text):
        # print(config.get('site', 'name'))
        APP_ID = config.get('baidu', 'app_id')
        API_KEY = config.get('baidu', 'app_key')
        SECRET_KEY = config.get('baidu', 'secret_key')

        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        # result = client.synthesis(text, 'zh', 1, {
        #     'vol': 11,
        # })
        # text = "床前明月光"

        # """ 调用DNN语言模型 """
        # print(client)
        return client.dnnlm(text)


     