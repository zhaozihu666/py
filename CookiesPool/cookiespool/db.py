#coding=gbk
import random
import redis
from cookiespool.config import *


class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        ��ʼ��Redis����
        :param host: ��ַ
        :param port: �˿�
        :param password: ����
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        ��ȡHash������
        :return: Hash����
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        ���ü�ֵ��
        :param username: �û���
        :param value: �����Cookies
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        ���ݼ�����ȡ��ֵ
        :param username: �û���
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        ���ݼ���ɾ����ֵ��
        :param username: �û���
        :return: ɾ�����
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        ��ȡ��Ŀ
        :return: ��Ŀ
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        ����õ���ֵ���������Cookies��ȡ
        :return: ���Cookies
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        ��ȡ�����˻���Ϣ
        :return: �����û���
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        ��ȡ���м�ֵ��
        :return: �û����������Cookies��ӳ���
        """
        return self.db.hgetall(self.name())


if __name__ == '__main__':
    conn = RedisClient('accounts', 'weibo')
    result = conn.set('hell2o', 'sss3s')
    print(result)