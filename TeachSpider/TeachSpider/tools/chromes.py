# -*- coding: utf-8 -*-
# @Time    : 2019/4/21 21:28
# @Author  : 郭增祥
# @File    : chromes-百度学术信息挖掘
import configparser
import os
import time
import zipfile
import string
from selenium import webdriver

class Proxy_chromes():
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_extension(self.getPlugins())
        self.set_chrome_options()
        # self.chromdriver_path = os.path.abspath(os.path.dirname(__file__)) + "\\chromedriver.exe"
        self.driver = webdriver.Chrome(options=self.option)

    def get_html(self, url):
        self.driver.get(url)
        # print(self.driver.page_source)
        return self.driver.page_source

    def get_chrome(self):
        return self.driver
    def getPlugins(self):
        # 读取配置文件
        cf = configparser.ConfigParser()
        config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\proxy.ini"
        cf.read(config_path)
        # 代理服务器
        proxy_host = cf.get("IP_Proxy_Config", "proxyHost")
        proxy_port = cf.get("IP_Proxy_Config", "proxyPort")
        # 代理隧道验证信息
        proxy_username = cf.get("IP_Proxy_Config", "proxyUser")
        proxy_password = cf.get("IP_Proxy_Config", "proxyPass")
        scheme = 'http'
        plugin_path = None
        # 创建一个代理chrome插件
        if plugin_path is None:
            plugin_path = os.getcwd() + r'/{}_{}@t.16yun.zip'.format(proxy_username, proxy_password)

        manifest_json = """
                           {
                               "version": "1.0.0",
                               "manifest_version": 2,
                               "name": "16YUN Proxy",
                               "permissions": [
                                   "proxy",
                                   "tabs",
                                   "unlimitedStorage",
                                   "storage",
                                   "<all_urls>",
                                   "webRequest",
                                   "webRequestBlocking"
                               ],
                               "background": {
                                   "scripts": ["background.js"]
                               },
                               "minimum_chrome_version":"22.0.0"
                           }
                           """

        background_js = string.Template(
            """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                }
              };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return plugin_path

    def set_chrome_options(self):
        self.option.add_argument('disable-infobars')
        self.option.add_argument('blink-settings=imagesEnabled=false')

    def quit(self):
        self.driver.quit()

class NoProxy_Chrome(object):
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.set_chrome_options()
        self.driver = webdriver.Chrome(options=self.option)

    def set_chrome_options(self):
        self.option.add_argument('disable-infobars')
        self.option.add_argument('blink-settings=imagesEnabled=false')

    def get_chrome(self):
        return self.driver

if __name__ == '__main__':
    chrome = NoProxy_Chrome().get_chrome()
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=62095104_26_oem_dg&wd=IP&rsv_pq=fce19186000c1560&rsv_t=780fn2RNJdwKpBcnXhbLn3K8XqMV7XaCT1dOzgR2QKxenOIkKuqnOzmuFQ5PpGFXeuHtwKdoTjew&rqlang=cn&rsv_enter=1&rsv_sug3=4&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=695&rsv_sug4=1662"
    chrome.get(url)