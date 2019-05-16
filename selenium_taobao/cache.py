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
        print('正在测试cookies','用户名'，username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('cookies不合法'，username)
            self.cookies_db.delete(username)
            print('删除COOKIES',username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code==200:
                print('cookies有效',username)
                print('部分测试结果',response.text[0:50])
            else:
                print(response.status_code,response.headers)
                print('cookies失败'，username)
                self.cookies_db.delete(username)
                print('删除COOKIES',username)
        except ConnectionAbortedError as e:
            print('发生异常',e.args)
#url,可替换和增加            
        TEST_URL_MAP = {
            'weibo':'https://m.weibo.cn/'
        }
        
        
class RedisClient(object):
    #----------------------------------------------------------------------
    def __init__(self,type,website,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化Redis连接池
        :param host:地址
        :param port:端口
        :param password:密码        
        """
        self.db = redis.StrictRedis(host = host,port= port, password=password,decode_responses=True)
        self.type = type
        self.website = website
            
    #----------------------------------------------------------------------
    def name(self):
        """
        获取Hash的名称
        ：return:Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)
    
    #----------------------------------------------------------------------
    def set(self,username,value):
        """
        设置键值对
        :param username:用户名
        :param value:密码或者Cookies
        :return:
        """
        return self.db.hset(self.name(),username,value)
    #----------------------------------------------------------------------
    def get(self,username):
        """
        根据键值对获取键值
        :param username:用户名
        :return:
        """
        return self.db.hget(self.name(),username)
    #----------------------------------------------------------------------
    def delete(self,username):
        """
        根据键名删除键值对
        :param username: 用户名
        :return:删除结果
        """
        return self.db.hdel(self.name(),username)
    
    #----------------------------------------------------------------------
    def count(self):
        """
        获取数目
        :return: 数目
        """
        return self.db.hlen(self.name())
    
    #----------------------------------------------------------------------
    def random(self):
        """
        随机得到键值，用于随机Cookies获取
        :return: 随机Cookies
        """
        return random.choice(self.db.hvals(self.name()))
    
    #----------------------------------------------------------------------
    def username(self):
        """
        获取所有账户信息
        :return:所有用户名
        """
        return self.db.hkeys(self.name())
    #----------------------------------------------------------------------
    def all(self):
        """
        获取所有键值对：
        :return: 用户名和密码或Cookies的映射表
        """
        return self.db.hgetall(self.name())
    
    #-生成模块---------------------------------------------------------------------
    def get_cookies(self):
        return self.browser.get_cookies()
        
    #----------------------------------------------------------------------
    def main(self):
        self.open()
        if self.password_error():
            return{
                'status':2,
                'content':'用户名或密码错误'
            }
        #如果不需要验证码直接登录
        if self.login_successfully():
            cookies = self.get_cookies()
            return{
                'status':1,
                'content':cookies
            }
        #获取验证码图片
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
                'content':'登陆失败'
            }

result = self.new_cookies(username, password)
#成功获取
if result.get('status') == 1:
    cookies = self.process_cookies(result.get('content'))
    print('成功获取到Cookies',cookies)
    if self.cookies_db.set(username,json,dump(cookies)):
        print('成功保存Cookies')
#密码错误，移除账号
elif result.get('status') == 2:
    print(result.get('content'))
    if self.accounts_db.delete(username):
        print('成功删除账号')
else:
    print(result.get('content'))
        
        
    
        
        
        
        
        