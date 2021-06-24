from data_process import data_process_1
from sklearn.model_selection import train_test_split#导入数据切分函数
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer#前者为转化词频向量函数，后者为转化tf-idf权重向量函数
from sklearn.naive_bayes import GaussianNB#导入高斯朴素贝叶斯分类器
from sklearn.metrics import f1_score
#=====库调用=====

#=====数据由自定义函数得到，并切分训练集和测试集数据
adata,data_after_stop,labels = data_process_1()
data_tr,data_te,labels_tr,labels_te = train_test_split(adata,labels,train_size=0.7)

#=====转化为稀疏矩阵后再转化为tf-idf权值向量
countVectorizer = CountVectorizer()#先构建一个对象以便测试样本使用
data_tr = countVectorizer.fit_transform(data_tr)#训练集的稀疏矩阵
X_tr = TfidfTransformer().fit_transform(data_tr.toarray()).toarray()#获得训练样本变量tf-idf权值

data_te = CountVectorizer(vocabulary=countVectorizer.vocabulary_).fit_transform(data_te)#测试集的稀疏矩阵(采用和训练集相同的词袋)
X_te = TfidfTransformer().fit_transform(data_te.toarray()).toarray()

#=====模型构建=====
model = GaussianNB()#导入高斯朴素贝叶斯分类器
model.fit(X_tr,labels_tr)#训练高斯朴素贝叶斯模型
model.score(X_te,labels_te)#模型检测