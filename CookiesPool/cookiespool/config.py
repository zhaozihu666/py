#coding=gbk
# Redis���ݿ��ַ
REDIS_HOST = 'localhost'

# Redis�˿�
REDIS_PORT = 6379

# Redis���룬������None
REDIS_PASSWORD = 'foobared'

# ������ʹ�õ������
BROWSER_TYPE = 'Chrome'

# �������࣬����չ����վ�㣬���ڴ�����
GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator'
}

# �����࣬����չ����վ�㣬���ڴ�����
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}

TEST_URL_MAP = {
    'weibo': 'https://m.weibo.cn/'
}

# ����������֤��ѭ������
CYCLE = 120

# API��ַ�Ͷ˿�
API_HOST = '0.0.0.0'
API_PORT = 5000

# ���������أ�ģ���¼���Cookies
GENERATOR_PROCESS = True
# ��֤�����أ�ѭ��������ݿ���Cookies�Ƿ���ã�������ɾ��
VALID_PROCESS = True    
# API�ӿڷ���
API_PROCESS = True