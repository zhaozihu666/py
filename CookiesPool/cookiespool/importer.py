#coding=gbk
import requests

from cookiespool.db import RedisClient

conn = RedisClient('accounts', 'weibo')

def set(account, sep='----'):
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('�˺�', username, '����', password)
    print('¼��ɹ�' if result else '¼��ʧ��')


def scan():
    print('�������˺�������, ����exit�˳�����')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()