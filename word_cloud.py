from data_process import data_process_1
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pylab

#=====导入背景图=====
mask = plt.imread('duihuakuan.jpg')

#=====词云图配置=====
wc = WordCloud(mask=mask,background_color='white',font_path=r'C:\Windows\Fonts\simhei.ttf')

adata,data_after_stop,labels = data_process_1()

#=====词云图的生成=====
word_fre = {}
for i in data_after_stop[labels == '劳动和社会保障']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('劳动和社会保障词云图.png')

word_fre = {}
for i in data_after_stop[labels == '城乡建设']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('城乡建设词云图.png')

word_fre = {}
for i in data_after_stop[labels == '教育文体']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('教育文体词云图.png')

word_fre = {}
for i in data_after_stop[labels == '卫生计生']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('卫生计生词云图.png')

word_fre = {}
for i in data_after_stop[labels == '交通运输']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('交通运输词云图.png')

word_fre = {}
for i in data_after_stop[labels == '商贸旅游']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('商贸旅游词云图.png')

word_fre = {}
for i in data_after_stop[labels == '环境保护']:
    for j in i:
        if j not in word_fre.keys():
            word_fre[j] = 1
        else:
            word_fre[j] += 1
wc.fit_words(word_fre)
plt.imshow(wc)
pylab.show()
wc.to_file('环境保护词云图.png')
