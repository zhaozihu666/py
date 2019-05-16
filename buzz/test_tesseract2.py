# coding=gbk
import requests
import time
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup

def captcha(data):
    with open('captcha.jpg','wb') as fp:
        fp.write(data)
    time.sleep(1)
    image = Image.open("captcha.jpg")
    text = pytesseract.image_to_string(image)
    print("����ʶ������֤��Ϊ��" + text)
    command = raw_input("������Y��ʾͬ��ʹ�ã��������������������룺")
    if (command == "Y" or command == "y"):
        return text
    else:
        return raw_input('������֤�룺')

def zhihuLogin(username,password):

    # ����һ������Cookieֵ��session����
    sessiona = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36'
}

    # �Ȼ�ȡҳ����Ϣ���ҵ���ҪPOST�����ݣ������Ѽ�¼��ǰҳ���Cookie��
    html = sessiona.get('https://www.zhihu.com/#signin', headers=headers).content

    # �ҵ� name ����ֵΪ _xsrf ��input��ǩ��ȡ��value���ֵ
    _xsrf = BeautifulSoup(html ,'lxml').find('input', attrs={'name':'_xsrf'}).get('value')

    # ȡ����֤�룬r�����ֵ��Unixʱ���,time.time()
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)
    response = sessiona.get(captcha_url, headers = headers)


    data = {
      "_xsrf":_xsrf,
    "email":username,
    "password":password,
    "remember_me":True,
    "captcha": captcha(response.content)
  }

    response = sessiona.post('https://www.zhihu.com/login/email', data = data, headers=headers)
    print (response.text)

    response = sessiona.get('https://www.zhihu.com/people/maozhaojun/activities', headers=headers)
    print (response.text)


if __name__ == "__main__":
    #username = raw_input("username")
    #password = raw_input("password")
    zhihuLogin('18882010971','zgh19970701')