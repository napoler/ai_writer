# 导入 webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys
import time
import re
import random
from bs4 import BeautifulSoup
from .config import CHROMEDRIVER,DEBUG
import logging

from cacheout import Cache
cache = Cache()

class BaiduSearch:
    def search(self,keyword,num = 10):
        try:
            s_data = self.search_first(keyword)
        except:
            print("搜索失败:"+keyword)
            return []
        if s_data:
            data = s_data['data']
            next_url = s_data['next_url']
            print("相关词为")
            print(s_data['kws'])
            kws = s_data['kws']
            n = 0
            while  n < num:
                print('下一页')
                print(n)
                logging.info(n)
                if len(next_url) >10:
                    t = random.randint(1,5)
                    # logging.info('搜索结束休息中 '+str(t)+'s')
                    # time.sleep(1)
                    try:
                        s_data = self.search_next(keyword,s_data['next_url'])
                    except:
                        print("搜索失败:"+keyword+str(n))
                        return False

                    data = data + s_data['data']

                    # print(s_data)
                    next_url = s_data['next_url']
                    print(next_url)

                n = n+1
                # next_url=''
            return data,kws
        else:
            return [],[]


    def search_first(self,keyword):
        key = 'baidu_'+keyword
        if cache.get(key) is None:

            # 创建chrome启动选项
            chrome_options = webdriver.ChromeOptions()

            # 指定chrome启动类型为headless 并且禁用gpu
            if DEBUG:
                print("开启了调试打开浏览器窗口")
            else:
                chrome_options.add_argument('--headless')

        #    prefs = {'profile.default_content_setting_values': {
        #                     'cookies': 2, 'images': 2, 'javascript': 2,
        #                     'plugins': 2, 'popups': 2, 'geolocation': 2,
        #                     'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
        #                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        #                     'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
        #                     'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
        #                     'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
        #                     'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
        #                     'durable_storage': 2}}
        #     chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument('--disable-gpu')

            # 调用环境变量指定的chrome浏览器创建浏览器对象
            driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=CHROMEDRIVER)

            # 如果没有在环境变量指定Chrome位置
            # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/wx/application/chromedriver')
            # keyword ="阿拉斯加雪撬犬 site:163.com"
            # get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
            # driver.get("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd="+keyword)
            # input_element = driver.find_element_by_name("wd")
            # input_element.send_keys(keyword)
            # input_element.submit()
            # input_element.send_keys(Keys.ENTER)
            # click_btn = driver.find_element_by_id("su")
            # click_btn.click()

            #发送请求
            driver.get("http://www.baidu.com")

            #进行页面截屏
            # driver.save_screenshot("./baidu.png")

            #元素定位的方法
            # driver.find_element_by_id("kw").send_keys("python")
            # # driver.find_element_by_id("su").click()

            # elem.send_keys(Keys.RETURN)
            # driver 获取html字符串
            # print(driver.page_source) #浏览器中elements的内容
            elem=driver.find_element_by_id('kw')
            elem.send_keys(keyword)
            elem.send_keys(Keys.RETURN)
        #   print(driver.current_url)
            logging.info('实际url为: '+driver.current_url)
            elem.send_keys(Keys.RETURN)
            #找到“百度一下”
            baidu_click=driver.find_element_by_id('su')
            #点击“百度一下”
            baidu_click.click()
            try:
                #最多等待10秒直到浏览器标题栏中出现我希望的字样（比如查询关键字出现在浏览器的title中）
                WebDriverWait(driver, 10).until(
                    expected_conditions.title_contains(keyword))
                print(driver.title)
                # print(driver.page_source)
                bsobj = BeautifulSoup(driver.page_source, 'html.parser')

                num_text_element = bsobj.find('span', {'class': 'nums_text'})
            #   print(num_text_element.text)
                logging.info(num_text_element.text)
                nums = filter(lambda s: s == ',' or s.isdigit(), num_text_element.text)
                # print(''.join(nums))
                #下一页链接
                next_url = bsobj.find('a', {'class': 'n'})
                #获取相关词
                rs = bsobj.find('div', {'id': 'rs'}).find_all('a')
                # kws = rs.find_all('a')
                print('相关关键词')
                kws=[]
                for kw in rs:

                    # print(kw)
                    kws.append(kw.get_text())
                    

                # elements = bsobj.findAll('div', {'class': re.compile('c-container')})
                elements = bsobj.findAll('div', {'class': re.compile('c-container')})
                # print('elements',len(elements))
                data =[]
                # BeautifulSoup(html, 'html.parser')   #文档对象
                for element in elements:
                    a= element.select('a')[0]
                    # t= element.select('.c-gap-top-small')
                    # print(t)
                    # print(element.select('a')[0].get_text())
                    # a=element.select('h3 > a').get_text()
                    # print(a[0]['href'])
                    # print(BeautifulSoup(a[0]).get_text())
                    # for it in a:
                    #     print(it[href])
                    # print("循环中",element.find('h3').find('a').get_text())
                #     a=element.find('h3').find('a')
                    item= {
                        # 'title':element.h3.a.text,
                        # 'url':element.h3.a['href']
                        'title':a.get_text(),
                        'url':a['href']
                        # 'text':t.get_text()
                    }
                #     logging.info(element.h3.a.text)
                #     print('获取资源： ', element.h3.a.text)
                #     # print('链接：', element.h3.a['href'])
                #     # print(
                #     #     '===============================================================')
                    data.append(item)

                full = {'data':data,
                        'kws':kws,
                        'next_url':'http://www.baidu.com'+next_url['href']
                        }
                logging.info(full)
            except:
                return False
            finally:
                #关闭浏览器
                driver.close()
            # full= driver(driver)

            print('创建新缓存')
            cache.set(key ,full)
        else:
            print('获取缓存')
            full = cache.get(key)

        return full
    def search_next(self,keyword,url):
        key = 'baidu_'+url
        if cache.get(key) is None:
            # 创建chrome启动选项
            chrome_options = webdriver.ChromeOptions()

            # 指定chrome启动类型为headless 并且禁用gpu
            if DEBUG:
                print("开启了调试打开浏览器窗口")
            else:
                chrome_options.add_argument('--headless')

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
            driver.get(url)

            try:
                #最多等待10秒直到浏览器标题栏中出现我希望的字样（比如查询关键字出现在浏览器的title中）
                WebDriverWait(driver, 10).until(
                    expected_conditions.title_contains(keyword))
                # print(driver.title)
                logging.info('加载成功网页: '+driver.title)
                bsobj = BeautifulSoup(driver.page_source,features="lxml")

                num_text_element = bsobj.find('span', {'class': 'nums_text'})
            #   print(num_text_element.text)
                logging.info(num_text_element.text)
                nums = filter(lambda s: s == ',' or s.isdigit(), num_text_element.text)
                # print(''.join(nums))
                #下一页链接
                next_url = bsobj.find('a', {'class': 'n'})




                elements = bsobj.findAll('div', {'class': re.compile('c-container')})


                data =[]
                for element in elements:
                    a= element.select('a')[0]
                    # t= element.select('.c-gap-top-small')[0]
                    # print(element.select('a')[0].get_text())
                    # a=element.select('h3 > a').get_text()
                    # print(a[0]['href'])
                    # print(BeautifulSoup(a[0]).get_text())
                    # for it in a:
                    #     print(it[href])
                    # print("循环中",element.find('h3').find('a').get_text())
                #     a=element.find('h3').find('a')
                    item= {
                        # 'title':element.h3.a.text,
                        # 'url':element.h3.a['href']
                        'title':a.get_text(),
                        'url':a['href']
                        # 'text':t.get_text()
                    }
                    # item= {
                    #     'title':element.h3.a.text,
                    #     'url':element.h3.a['href']

                    # }
                    # print('获取资源： ', element.h3.a.text)
                    # print('链接：', element.h3.a['href'])
                    # print(
                    #     '===============================================================')
                    data.append(item)

                full = {'data':data,
                        'next_url':'http://www.baidu.com'+next_url['href']
                        }
            except:
                return False
            finally:
                #关闭浏览器
                driver.close()

            print('创建新缓存')
            cache.set(key ,full)
        else:
            print('获取缓存')
            full = cache.get(key)

        return full



  # def search_item(driver):
  #     try:
  #         #最多等待10秒直到浏览器标题栏中出现我希望的字样（比如查询关键字出现在浏览器的title中）
  #         WebDriverWait(driver, 10).until(
  #             expected_conditions.title_contains(keyword))
  #         # print(driver.title)
  #         bsobj = BeautifulSoup(driver.page_source)

  #         num_text_element = bsobj.find('span', {'class': 'nums_text'})
  #         print(num_text_element.text)
  #         nums = filter(lambda s: s == ',' or s.isdigit(), num_text_element.text)
  #         # print(''.join(nums))

  #         elements = bsobj.findAll('div', {'class': re.compile('c-container')})
  #         data =[]
  #         for element in elements:
  #             item= {
  #                 'title':element.h3.a.text,
  #                 'url':element.h3.a['href']

  #             }
  #             # print('标题：', element.h3.a.text)
  #             # print('链接：', element.h3.a['href'])
  #             # print(
  #             #     '===============================================================')
  #             data.append(item)
  #         full = data

  #     finally:
  #         #关闭浏览器
  #         driver.close()


  #     return full


      #driver获取cookie
      # cookies = driver.get_cookies()
      # print(cookies)
      # print("*"*100)
      # cookies = {i["name"]:i["value"] for i in cookies}
      # print(cookies)
      # print(driver.page_source) #浏览器中elements的内容

      # driver.save_screenshot("./baidu1.png")
      # #退出浏览器
      # time.sleep(3)
      # driver.quit()
 # d = search(keyword="柯基犬",num=2)


#print(d)
