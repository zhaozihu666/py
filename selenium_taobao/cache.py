# coding=gbk
import random
import redis
import json
import requests
from requests.exceptions import connectionError


class ValidTester(object):
    #----------------------------------------------------------------------
    def __init__(self,website='defult'):
        self.website = website
        self.cookies_db = RedisClient('cookies',self.website)
        self.accounts_db = RedisClient('accounts',self.website)
    #----------------------------------------------------------------------
    def test(self):
        raise NotImplementedError
        
    #----------------------------------------------------------------------
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username,cookies in cookies_groups.items():
            self.test(username,cookies)
        
class WeiboValidTester(ValidTester):
    #----------------------------------------------------------------------
    def __init__(self):
        ValidTester.__init__(self,website)
        
    def test(self,username,cookies):
        print('���ڲ���cookies','�û���'��username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('cookies���Ϸ�'��username)
            self.cookies_db.delete(username)
            print('ɾ��COOKIES',username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code==200:
                print('cookies��Ч',username)
                print('���ֲ��Խ��',response.text[0:50])
            else:
                print(response.status_code,response.headers)
                print('cookiesʧ��'��username)
                self.cookies_db.delete(username)
                print('ɾ��COOKIES',username)
        except ConnectionAbortedError as e:
            print('�����쳣',e.args)
#url,���滻������            
        TEST_URL_MAP = {
            'weibo':'https://m.weibo.cn/'
        }
        
        
class RedisClient(object):
    #----------------------------------------------------------------------
    def __init__(self,type,website,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        ��ʼ��Redis���ӳ�
        :param host:��ַ
        :param port:�˿�
        :param password:����        
        """
        self.db = redis.StrictRedis(host = host,port= port, password=password,decode_responses=True)
        self.type = type
        self.website = website
            
    #----------------------------------------------------------------------
    def name(self):
        """
        ��ȡHash������
        ��return:Hash����
        """
        return "{type}:{website}".format(type=self.type, website=self.website)
    
    #----------------------------------------------------------------------
    def set(self,username,value):
        """
        ���ü�ֵ��
        :param username:�û���
        :param value:�������Cookies
        :return:
        """
        return self.db.hset(self.name(),username,value)
    #----------------------------------------------------------------------
    def get(self,username):
        """
        ���ݼ�ֵ�Ի�ȡ��ֵ
        :param username:�û���
        :return:
        """
        return self.db.hget(self.name(),username)
    #----------------------------------------------------------------------
    def delete(self,username):
        """
        ���ݼ���ɾ����ֵ��
        :param username: �û���
        :return:ɾ�����
        """
        return self.db.hdel(self.name(),username)
    
    #----------------------------------------------------------------------
    def count(self):
        """
        ��ȡ��Ŀ
        :return: ��Ŀ
        """
        return self.db.hlen(self.name())
    
    #----------------------------------------------------------------------
    def random(self):
        """
        ����õ���ֵ���������Cookies��ȡ
        :return: ���Cookies
        """
        return random.choice(self.db.hvals(self.name()))
    
    #----------------------------------------------------------------------
    def username(self):
        """
        ��ȡ�����˻���Ϣ
        :return:�����û���
        """
        return self.db.hkeys(self.name())
    #----------------------------------------------------------------------
    def all(self):
        """
        ��ȡ���м�ֵ�ԣ�
        :return: �û����������Cookies��ӳ���
        """
        return self.db.hgetall(self.name())
    
    #-����ģ��---------------------------------------------------------------------
    def get_cookies(self):
        return self.browser.get_cookies()
        
    #----------------------------------------------------------------------
    def main(self):
        self.open()
        if self.password_error():
            return{
                'status':2,
                'content':'�û������������'
            }
        #�������Ҫ��֤��ֱ�ӵ�¼
        if self.login_successfully():
            cookies = self.get_cookies()
            return{
                'status':1,
                'content':cookies
            }
        #��ȡ��֤��ͼƬ
        image = self.get_image('captcha.png')
        numbers = self.detect_image(image)
        self.move(numbers)
        if self.login_successfully():
            cookies = self.get_cookies()
            return{
                'status':1,
                'content':cookies
            }
        else:
            return{
                'status':3,
                'content':'��½ʧ��'
            }

result = self.new_cookies(username, password)
#�ɹ���ȡ
if result.get('status') == 1:
    cookies = self.process_cookies(result.get('content'))
    print('�ɹ���ȡ��Cookies',cookies)
    if self.cookies_db.set(username,json,dump(cookies)):
        print('�ɹ�����Cookies')
#��������Ƴ��˺�
elif result.get('status') == 2:
    print(result.get('content'))
    if self.accounts_db.delete(username):
        print('�ɹ�ɾ���˺�')
else:
    print(result.get('content'))
        
        
    
        
        
        
        
        