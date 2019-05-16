# -*-coding:utf-8-*-  
from PIL import Image  
import sys  
import os  
import pytesseract
from selenium import webdriver  

url = '网站地址'
driver = webdriver.Chrome()
driver.maximize_window()  # 将浏览器最大化
driver.get(url)
# 截取当前网页并放到E盘下命名为printscreen，该网页有我们需要的验证码
driver.save_screenshot('E:\\printscreen.png') 
imgelement = driver.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
size = imgelement.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
im = Image.open("E:\\printscreen.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save('E:\\save.jpg') # 保存我们接下来的验证码图片 进行打码
#转化到灰度图
imgry = im.convert('L')
#保存图像
imgry.save('g'+name)
#二值化，采用阈值分割法，threshold为分割点
threshold = 140
table = []
for j in range(256):
    if j < threshold:
        table.append(0)
    else:
        table.append(1)
out = imgry.point(table, '1')
out.save('b'+name)
#识别
text = pytesseract.image_to_string(out)
#识别对吗
text = text.strip()
text = text.upper();
print (text)
text = pytesseract.image_to_string(Image.open('E:\\printscreen.png'), lang="eng")
print(text)  
