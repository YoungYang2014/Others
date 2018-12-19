# -*- coding: utf-8 -*-
import requests
import traceback

class WebDownloader(object):
    """http下载器，对requests简单封装及自动维护cookie"""
    def __init__(self):
        '''创建session，维护cookie'''
        self.headers = {
                            "Accept-Language": "zh-CN,zh;q=0.9",
                            "Connection": "keep-alive",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
                        }
        # 创建opener管理cookie
        self.opener = requests.session()

    def http_post(self, url, post_data):
        """
        post方法封装
        :return http code，response
        """
        try:
            response = self.opener.post(url, post_data, headers=self.headers, timeout=3)
            return response.status_code, response.text
        except:
            return False, traceback.format_exc()

    def http_get(self, url):
        """
        get方法封装
        :return http code，response
        """
        try:
            response = self.opener.get(url, headers=self.headers, timeout=3)
            return response.status_code, response.text
        except:
            return False, traceback.format_exc()

if __name__=="__main__":
    pass