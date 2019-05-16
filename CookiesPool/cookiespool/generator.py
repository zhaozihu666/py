#coding=gbk
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookiespool.config import *
from cookiespool.db import RedisClient
from login.weibo.cookies import WeiboCookies


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        ����, ��ʼ��һЩ����
        :param website: ����
        :param browser: �����, ����ʹ��������������Ϊ None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    def __del__(self):
        self.close()
    
    def init_browser(self):
        """
        ͨ��browser������ʼ��ȫ���������ģ���¼ʹ��
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            self.browser = webdriver.Chrome()
    
    def new_cookies(self, username, password):
        """
        ������Cookies��������Ҫ��д
        :param username: �û���
        :param password: ����
        :return:
        """
        raise NotImplementedError
    
    def process_cookies(self, cookies):
        """
        ����Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict
    
    def run(self):
        """
        ����, �õ������˻�, Ȼ��˳��ģ���¼
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()
        
        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('��������Cookies', '�˺�', username, '����', password)
                result = self.new_cookies(username, password)
                # �ɹ���ȡ
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('�ɹ���ȡ��Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('�ɹ�����Cookies')
                # ��������Ƴ��˺�
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('�ɹ�ɾ���˺�')
                else:
                    print(result.get('content'))
        else:
            print('�����˺Ŷ��Ѿ��ɹ���ȡCookies')
    
    def close(self):
        """
        �ر�
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self, website='weibo'):
        """
        ��ʼ������
        :param website: վ������
        :param browser: ʹ�õ������
        """
        CookiesGenerator.__init__(self, website)
        self.website = website
    
    def new_cookies(self, username, password):
        """
        ����Cookies
        :param username: �û���
        :param password: ����
        :return: �û�����Cookies
        """
        return WeiboCookies(username, password, self.browser).main()


if __name__ == '__main__':
    generator = WeiboCookiesGenerator()
    generator.run()