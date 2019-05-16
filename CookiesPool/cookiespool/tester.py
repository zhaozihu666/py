#coding=gbk
import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, username, cookies):
        raise NotImplementedError
    
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)
    
    def test(self, username, cookies):
        print('���ڲ���Cookies', '�û���', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies���Ϸ�', username)
            self.cookies_db.delete(username)
            print('ɾ��Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies��Ч', username)
            else:
                print(response.status_code, response.headers)
                print('CookiesʧЧ', username)
                self.cookies_db.delete(username)
                print('ɾ��Cookies', username)
        except ConnectionError as e:
            print('�����쳣', e.args)

if __name__ == '__main__':
    WeiboValidTester().run()