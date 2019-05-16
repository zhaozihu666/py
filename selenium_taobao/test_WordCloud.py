# coding=gbk
from wordcloud import WordCloud


wcd = WordCloud(background_color='white')
text = "富强 民主 文明 和谐 自由 平等 公正 法治 爱国 敬业 诚信 友善 "
wcd.generate(text)
wcd.to_image()