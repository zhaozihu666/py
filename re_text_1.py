#coding=utf8
import re

a = """
<input totime="1546258654000"  istop="" type="checkbox" unread=false   fn="Angela(QQ邮箱产品经理)" fa="Angela_admin@qq.com" name="mailid" value="ZC1831-ObtlL15WQA4kT14CNgc8H8c""/>  <input totime="1545720163000"  istop="" type="checkbox" unread=false   fn="标题" fa="estmtservice@eb.spdbccc.com.cn" name="mailid" value="ZC1125-NbfUscARXhAxYnMv8dYAC8c" colid="-145288728" adconv="0" ssystag="system:1|friend:0|important:0|"/></td> <u tabindex="0" class="black tt ">标题</u><b class="no " >&nbsp;-&nbsp;&nbsp;真实内容</b>&nbsp;</div>

"""
pattern2 = re.compile(
    'totime="(.*?)".*?fn="(.*?)".*?fa="(.*?)".*?value="(.*?)".+<u tabindex="0" class="black tt ">(.*?)</u>.*?<b class="no "[ ]?>(.*?)</b>')
mails = re.findall(pattern2, a)
email_list = []
for mail in mails:
    key_list = [""]
    for key in key_list:
        if key in mail[1]:
            rest = (mail[0], mail[1], mail[2], mail[3], mail[4], mail[5])
            email_list.append(rest)

for i in email_list:
    print(i)