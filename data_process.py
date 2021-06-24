import pandas as pd
import numpy as np
import re
import jieba
#引入第三方库
#第一题数据处理
def data_process_1(file = 'data.xlsx'):
    data = pd.read_excel(file)
    data = data.drop(labels=['留言编号','留言用户','留言主题','留言时间'],axis=1)#只留下留言详情和留言分类
    data = data.rename(columns={'留言详情':'message','一级标签':'label'})#将留言详情和一级分类的列名称改为message和label
    data['label'].value_counts()#对label进行计算

    n = 613#定义抽样条数

    #=====对七大一级标签进行抽样=====
    a = data[data['label'] == '劳动和社会保障'].sample(n)
    b = data[data['label'] == '城乡建设'].sample(n)
    c = data[data['label'] == '教育文体'].sample(n)
    d = data[data['label'] == '卫生计生'].sample(n)
    e = data[data['label'] == '交通运输'].sample(n)
    f = data[data['label'] == '商贸旅游'].sample(n)
    g = data[data['label'] == '环境保护'].sample(n)

    #=====抽取数据后的的dataframe进行合并=====
    data_new = pd.concat([a,b,c,d,e,f,g],axis=0)#抽样后的数据进行拼接后的新数据

    #=====对数据进行清洗=====
    data_dup = data_new['message'].drop_duplicates()#将新数据中的可能重复的数据直接进行删除留一个
    data_qumin = data_dup.apply(lambda x: re.sub(r'\s|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9|\*|\n|\t|\u3000','',x))#对数据中数字，字母等进行脱敏以及对转义字符进行去除
    data_qumin.shape

    #=====对数据进行分词（采用jieba分词）=====
    data_cut = data_qumin.apply(lambda x:jieba.lcut(x))#对每条数据进行分词，分词后返回列表

    #=====去除停用词=====
    stopWords = pd.read_csv('stopword.txt',encoding='UTF-8',sep='haha',engine='python',header=None)#读入停用词表
    stopWords = ['所长','、','：',' ','(',')','的','\\','{','}','!','《','》','年','月','日','尊敬','书记','市长','一名','您好','你好','市'] + list(stopWords.iloc[:,0])#将一些新词加入停用词表中
    data_after_stop = data_cut.apply(lambda x: [i for i in x if i not in stopWords])

    #=====封装函数返回值准备=====
    labels = data_new.loc[data_after_stop.index,'label']#通过对处理后的message序号去获取相对应的标签
    adata = data_after_stop.apply(lambda x: ' '.join(x))#data_after_stop是个列表通过空格将句子分割

    #=====函数返回值=====
    return adata,data_after_stop,labels

    #第二题数据处理
def data_process_2(file = 'data2.xlsx'):
    data2 = pd.read_excel(file)#读取数据文件
    data2_title = data2.drop(labels=['留言编号','留言用户','留言时间','留言详情','点赞数','反对数'],axis=1)#单独提出留言主题以便命名实体的提取
    data2_message = data2.drop(labels=['留言编号','留言用户','留言时间','留言主题','点赞数','反对数'],axis=1)#单独提出留言详情以便分词以及相似度计算
    data2_like = data2.drop(labels=['留言编号','留言用户','留言时间','留言主题','留言详情','反对数'],axis=1)
    data2_unlike = data2.drop(labels=['留言编号','留言用户','留言时间','留言主题','留言详情','点赞数'],axis=1)#单独提出点赞数和反对数以便之后热度指标量化的方便
    data2_time = data2.drop(labels=['留言编号','留言用户','留言主题','留言详情','点赞数','反对数'],axis=1)#单独提出时间以便之后的时间范围比较

    #=====数据清洗=====(针对data2中的留言详情）
    data2_message_qumin = data2_message['留言详情'].apply(lambda x: re.sub(r'\s|\t|\*','',x))#对数据中数字，字母等进行脱敏以及对转义字符进行去除

    #=====进行分词=====(针对data2中的留言详情）
    data2_message_cut = data2_message_qumin.apply(lambda x: jieba.lcut(x))  # 对每条数据进行分词，分词后返回列表

    #=====去除停用词=====(针对data2中的留言详情）
    stopWords = pd.read_csv('stopword.txt', encoding='UTF-8', sep='haha', engine='python', header=None)  # 读入停用词表
    stopWords = ['所长', '、', '：', ' ', '(', ')', '的', '\\', '{', '}', '!', '《', '》', '年', '月', '日', '尊敬', '书记', '市长', '一名',
                 '您好', '你好', '市','局长','区'] + list(stopWords.iloc[:, 0])  # 将一些新词加入停用词表中
    data2_message_after_stop = data2_message_cut.apply(lambda x: [i for i in x if i not in stopWords])

    adata = data2_message_after_stop.apply(lambda x: ' '.join(x))

    data2_title_list = np.array(data2_title)#留言主题列表
    data2_title_list = data2_title_list.tolist()

    number = len(data2)  # 获取数据总数以便之后循环范围确定
    return data2_like,data2_unlike,data2_title,data2_title_list,data2_message,number,data2,data2_time

def data_process_3(file = 'data3.xlsx'):
    data3 = pd.read_excel(file)
    data3_question = data3.drop(labels=['留言编号','留言用户','留言主题','留言时间','答复意见','答复时间'],axis=1)
    data3_answer = data3.drop(labels=['留言编号','留言用户','留言主题','留言时间','留言详情','答复时间'],axis=1)
    return data3,data3_question,data3_answer