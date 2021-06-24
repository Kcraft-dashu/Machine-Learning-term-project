from data_process import data_process_3
import pandas as pd
import jieba.analyse

data3,data3_question,data3_answer = data_process_3()
#=====留言详情、答复意见去空=====
for i in range(len(data3)):
    data3_question.loc[i,'留言详情'] = data3_question.loc[i,'留言详情'].replace('\n','')
    data3_question.loc[i, '留言详情'] = data3_question.loc[i, '留言详情'].replace('\t', '')
    data3_question.loc[i, '留言详情'] = data3_question.loc[i, '留言详情'].replace('\u3000', '')
    data3_question.loc[i, '留言详情'] = data3_question.loc[i, '留言详情'].replace('\xa0', '')
    data3_question.loc[i, '留言详情'] = data3_question.loc[i, '留言详情'].replace(' ', '')
    data3_answer.loc[i, '答复意见'] = data3_answer.loc[i, '答复意见'].replace('\n', '')
    data3_answer.loc[i, '答复意见'] = data3_answer.loc[i, '答复意见'].replace('\t', '')
    data3_answer.loc[i, '答复意见'] = data3_answer.loc[i, '答复意见'].replace('\u3000', '')
    data3_answer.loc[i, '答复意见'] = data3_answer.loc[i, '答复意见'].replace('\xa0', '')
    data3_answer.loc[i, '答复意见'] = data3_answer.loc[i, '答复意见'].replace(' ', '')

data3_answer_cut_list = []
for i in range(len(data3_answer)):
    cut = jieba.lcut(data3_answer.loc[i,'答复意见'])
    data3_answer_cut_list.append(cut)
#=====创建评价指标表=====
evaluation_df = pd.DataFrame(columns=['相关性','完整性','规范性'])
#=====相关性=====
for i in range(len(data3)):
    flag = 0
    question_keys = jieba.analyse.extract_tags(data3_question.loc[i,'留言详情'],topK=15)
    answer_keys = jieba.analyse.extract_tags(data3_answer.loc[i,'答复意见'],topK=15)
    for x in range(len(question_keys)):
        for y in range(len(answer_keys)):
            if question_keys[x] == answer_keys[y]:
                evaluation_df.loc[i,'相关性'] = '√'
                flag = 1
                break
    if flag == 0:
        evaluation_df.loc[i, '相关性'] = '×'
    question_keys.clear()
    answer_keys.clear()

#=====完整性=====
for i in range(len(data3)):
    if evaluation_df.loc[i,'相关性'] == '×':
        evaluation_df.loc[i,'完整性'] = '×'
        evaluation_df.loc[i,'规范性'] = '×'
    elif evaluation_df.loc[i,'相关性'] == '√':
        index = len(data3_question.loc[i,'留言详情']) * 1.2
        if len(data3_answer.loc[i,'答复意见']) < index:
            evaluation_df.loc[i,'完整性'] = '×'
        else:
            evaluation_df.loc[i,'完整性'] = '√'

#=====规范性=====
words = ['您好','感谢','收悉','谢谢','如下','回复','关心','监督','支持','理解','予以','你好','获悉']

for x in range(len(data3_answer_cut_list)):
    if evaluation_df.loc[x,'规范性'] == '×':
        continue
    else:
        flag2 = 0
        for y in data3_answer_cut_list[x]:
            for i in words:
                if y == i:
                    evaluation_df.loc[x,'规范性'] = '√'
                    flag2 = 1
                    break
        if flag2 == 0:
            evaluation_df.loc[x,'规范性'] = '×'

evaluation = pd.concat([data3,evaluation_df],axis=1)
evaluation_df.to_excel('答复意见质量评价表.xlsx',index=None)
evaluation.to_excel('直观答复意见质量评价表.xlsx',index=None)