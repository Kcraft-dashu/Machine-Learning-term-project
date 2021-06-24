from data_process import data_process_2
import synonyms
import hanlp
import pandas as pd
import numpy as np
import time
import datetime
#=====调用库=====

#=====自定义时间比较函数=====
def compare_time_min(time_1,time_2):#返回最旧的时间
    if time_1 and time_2:
        time_stamp_1 = time.mktime(time.strptime(time_1,'%Y/%m/%d %H:%M:%S'))
        time_stamp_2 = time.mktime(time.strptime(time_2,'%Y/%m/%d %H:%M:%S'))
        if int(time_stamp_1) > int(time_stamp_2):
            return time_2
        else:
            return time_1
    else:
        return None

def compare_time_max(time_1,time_2):#返回最新的时间
    if time_1 and time_2:
        time_stamp_1 = time.mktime(time.strptime(time_1,'%Y/%m/%d %H:%M:%S'))
        time_stamp_2 = time.mktime(time.strptime(time_2,'%Y/%m/%d %H:%M:%S'))
        if int(time_stamp_1) > int(time_stamp_2):
            return time_1
        else:
            return time_2
    else:
        return None
#=====由自定义函数获得数据=====
data2_like,data2_unlike,data2_title,data2_title_list,data2_message,number,data2,data2_time = data_process_2()

#=====根据data2的留言主题进行相似度比较以便问题的归并=====
list3 = []#存放最初筛选出的相似的问题的空列表
new_list = []
for x in range(number):
    list1 = []#创建空列表
    x_sen = ''.join(data2_title_list[x])
    for y in range(number):
        y_sen = ''.join(data2_title_list[y])
        r = synonyms.compare(x_sen,y_sen,seg=False)
        if r >= 0.75:list1.append([y])
        list2 = [y for x in list1 for y in x]
        #print(x_sen,'vs',y_sen,'的相似度为',r)
    list3.append(list2)
#测试点print(list3)

#=====对数据进行去重=====
for item in list3:
    if item not in new_list:
        new_list.append(item)
new_list = sorted(new_list,key=lambda i:len(i),reverse=True)#根据子列表元素个数进行从小到大排序
l2 = new_list[:]
for x in new_list:
    for y in new_list:
        if set(x).issubset(set(y)) and x != y:
            l2.remove(x)
            break
# 测试点print(l2)

#=====计算同类问题个数=====
count = []#=====创建count空列表用来存放同类问题个数
for x in range(len(l2)):
    count.append(len(l2[x]))
#测试点print(count)

#=====计算同类问题的点赞数和反对数=====
#计算点赞和反对的总数
feedback = 0
feedback_list = []#创建feedback空列表索引与问题同类型列表一级索引相同
for x in range(len(l2)):
    for y in l2[x]:
        feedback = feedback+data2_like.iloc[y,0] - data2_unlike.iloc[y,0]
    feedback_list.append(feedback)
    feedback = 0
    #测试点print(feedback_list)

#=====热度指标量化（占比 同类问题数目:反馈数=6:4）=====
hot_list = []#创建存放热度指数的空列表索引与问题同类型列表一级索引相同
hot = 0
for x in range(len(l2)):
    hot = count[x]*0.6+feedback_list[x]*0.4
    hot_list.append(hot)
    hot = 0
#将热度列表按热度指标进行排序得到索引
hot_array = np.array(hot_list)
index = np.argsort(hot_array)
index_list = index.tolist()#得到按热度指标排序的索引列表

#=====命名实体识别=====
recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
name_list = []
str =''#创建空字符串用于命名实体存放
for x in range(len(l2)):
    name = recognizer(data2_title_list[l2[x][0]][0])
    for x in range(len(name)):
        if(name[x][1]=='NS' or name[x][1]=='NT' or name[x][1]=='NR'):
            str = str+name[x][0]
    name_list.append(str)
    str =''#将命名实体添加至列表后将其清空

#=====时间提取=====
time_list = []
temp_list =[]
for x in range(len(l2)):
    for y in l2[x]:
        if type(data2_time.loc[y,'留言时间']) == datetime.datetime:
            time_stamp = data2_time.loc[y, '留言时间']
            time_str = time_stamp.strftime('%Y/%m/%d %H:%M:%S')
        else:
            time_str = data2_time.loc[y, '留言时间']
        temp_list.append(time_str)
    time_list.append(temp_list)
    temp_list = []

#=====时间范围提取=====
time_range_list = []
for x in range(len(time_list)):
    min_time = time_list[x][0]#初始化min_time以便之后与
    max_time = time_list[x][0]#初始化min_time以便之后与
    for y in time_list[x]:
        min_time = compare_time_min(min_time,y)
        max_time = compare_time_max(max_time,y)
    temp_list.append(min_time)
    temp_list.append(max_time)
    time_range_list.append(temp_list)
    temp_list = []
    # 测试点print('最早时间:',min_time)
    # 测试点print('最新时间:',max_time)

#=====创建空白表=====
hot_issues_df = pd.DataFrame(columns=['热度排名','问题ID','热度指数','时间范围','地点/人群','问题描述'])#创建热点问题表
hot_issues_detail_df = pd.DataFrame(columns=['问题ID','留言编号','留言用户','留言主题','留言时间','留言详情','点赞数','反对数'])#创建热点问题留言明细表
#=====数据写入=====
#=====热点问题表数据写入=====
for x in range(15):#热度排名和问题ID的写入
    hot_issues_df.loc[x,'热度排名'] = x + 1
    hot_issues_df.loc[x, '问题ID'] = x + 1
for x in range(-1,-16,-1):
    hot_issues_df.loc[-1 * x - 1,'热度指数'] = hot_list[index_list[x]]#热度指数写入
    hot_issues_df.loc[-1 * x - 1,'地点/人群'] = name_list[index_list[x]]#地点/人群写入
    hot_issues_df.loc[-1 * x - 1,'问题描述'] = data2_title.loc[l2[index_list[x]][0],'留言主题']#留言主题写入
    str_min = time_range_list[index_list[x]][0]
    str_max = time_range_list[index_list[x]][1]
    hot_issues_df.loc[-1 * x - 1,'时间范围'] = str_min[0:-9]+'至'+str_max[0:-9]

#=====热点问题留言明细表数据写入=====
row = -1#行索引初始值为-1 以便自增运算能以0为开始
id = 0
for y in range(-1,-16,-1):
    id = id + 1
    for z in l2[index_list[y]]:
        #测试点print(z)
        row = row + 1
        hot_issues_detail_df.loc[row,'问题ID'] = id
        hot_issues_detail_df.loc[row,'留言编号'] = data2.loc[z,'留言编号']
        hot_issues_detail_df.loc[row, '留言用户'] = data2.loc[z, '留言用户']
        hot_issues_detail_df.loc[row, '留言主题'] = data2.loc[z, '留言主题']
        hot_issues_detail_df.loc[row, '留言时间'] = data2.loc[z, '留言时间']
        hot_issues_detail_df.loc[row, '留言详情'] = data2.loc[z, '留言详情']
        hot_issues_detail_df.loc[row, '点赞数'] = data2.loc[z, '点赞数']
        hot_issues_detail_df.loc[row, '反对数'] = data2.loc[z, '反对数']

#=====导出数据生成xlsx文件=====
hot_issues_df.to_excel('热点问题表.xlsx',index=None)
hot_issues_detail_df.to_excel('热点问题留言明细表.xlsx',index=None)