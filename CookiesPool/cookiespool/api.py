#coding=gbk
import json
from flask import Flask, g
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    ��ȡ
    :return:
    """
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    ��ȡ�����Cookie, ���ʵ�ַ�� /weibo/random
    :return: ���Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    ����û�, ���ʵ�ַ�� /weibo/add/user/password
    :param website: վ��
    :param username: �û���
    :param password: ����
    :return: 
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    ��ȡCookies����
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')