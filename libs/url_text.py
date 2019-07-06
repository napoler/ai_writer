# 导入 webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys
import time
import re
from bs4 import BeautifulSoup
from .config import CHROMEDRIVER,DEBUG
import logging
from cacheout import Cache
cache = Cache()
# import requests
# import requests
from readability import Document
import html2text

import Terry_toolkit as tkit
import timeout_decorator

class UrlText:

    def get_text(self,url ):
        try:
            html = self.url_html(url)
        except:
            print("获取网页失败:"+url)
            return []
        ttext = tkit.Text()
        # nt = ttext.clear(text)
        #删除空行

        text = ttext.html_text(html)
        # text = ttext.remove_word_wrap(text)
        text = ttext.clear(text)
        return text
    # def remove_HTML_tag(self,tag, string):
    #     """删除特定的标签


    #     """
    #     string = re.sub(r"<\b(" + tag + r")\b[^>]*>", r"", string)
    #     return re.sub(r"<\/\b(" + tag + r")\b[^>]*>", r"", string)
    # def html_text(self,html):
    #     # response = requests.get(url)
    #     # logging.info(response.text)
    #     # html = request.urlopen(url)

    #     # logging.info(html)

    #     doc = Document(html)
    #     # doc = Document(html)
    #     # logging.info(doc.title())

    #     html= doc.summary(True)
    #     #   logging.info(doc.get_clean_html())
    #     # t =html2text.html2text(html)
    #     text_maker = html2text.HTML2Text()
    #     text_maker.ignore_links = True
    #     text_maker.bypass_tables = False
    #     text_maker.ignore_images = True
    #     text_maker.images_to_alt = True
    #     # html = function_to_get_some_html()
    #     text = text_maker.handle(html)
    #     text=self.remove_HTML_tag('img',text)
    #     # print(text)
    #     return text
    @timeout_decorator.timeout(30)
    def url_html(self,url):
        key = url
        if cache.get(key) is None:

            # 创建chrome启动选项
            chrome_options = webdriver.ChromeOptions()

            # 指定chrome启动类型为headless 并且禁用gpu
            if DEBUG:
                print("开启了调试打开浏览器窗口")
            else:
                chrome_options.add_argument('--headless')
            #屏蔽图片加载
            #prefs = {"profile.managed_default_content_settings.images": 2}
            prefs = {'profile.default_content_setting_values': {
                                        'cookies': 2, 'images': 2, 'javascript': 2,
                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                        'durable_storage': 2}}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--disable-gpu')

            # 调用环境变量指定的chrome浏览器创建浏览器对象
            driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=CHROMEDRIVER)
            # driver.set_timeout(30) # seconds
            #发送请求
            logging.info('开始加载页面: '+url)

            html = ''
            try:
                driver.get(url)
                #最多等待10秒直到浏览器标题栏中出现我希望的字样（比如查询关键字出现在浏览器的title中）
                # WebDriverWait(driver, 10).until(
                #     expected_conditions.title_contains(keyword))
                time.sleep(3)
                print('采集网页: '+driver.title)
                logging.info('加载成功网页: '+driver.title)
                html = driver.page_source #浏览器中elements的内容
            except:
                return False
            finally:

                print ("当前url为: "+driver.current_url)  # current_url 方法可以得到当前页面的URL

                #关闭浏览器
                driver.close()
            print('创建新缓存')
            # zy = Summarynew.Summary()
            # content = zy.search(keyword=keyword,num=int(num))
            #html = []
            cache.set(key ,html)
        else:
            print('获取缓存')
            html = cache.get(key)


        return html

    # def content
# ut = UrlText()
# url= "http://www.baidu.com/link?url=RosX1iVIyGGkaNKwndNTiZ2dSOoTT4BLLTxfyhFmzfGihgfws81VaGHrmBLhiHOnQzoYim-o9f16xd20aDTA8_"
# html = ut.url_html(url)
# print(html)
