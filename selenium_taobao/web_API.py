import json 
from flask import Flask, g
app = Flask(__name__)
#����ģ��������ֵ�
GENERATOR_MAP = {
    'weibo':'WeiboCookiesGenerator'
}
@app.route('/')
#----------------------------------------------------------------------
def index():
    return '<h2>Welecome to Cookies Pool System</h2>'

#----------------------------------------------------------------------
def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g,website):
            setattr(g,website + '_cookies',eval('RedisClient' + '("cookies","' + website +'")'))
    return g
@app.route('/<website>/random')
#----------------------------------------------------------------------
def random(website):
    """
    ��ȡ�����Cookies�����ʵ�ַ��/weibo/random
    :return: ���Cookies
    """
    g = get_conn()
    cookies = getattr(g,website+'_cookies').random()
    return cookies
    