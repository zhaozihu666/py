# coding=gbk
from wordcloud import WordCloud


wcd = WordCloud(background_color='white')
text = "��ǿ ���� ���� ��г ���� ƽ�� ���� ���� ���� ��ҵ ���� ���� "
wcd.generate(text)
wcd.to_image()