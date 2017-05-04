
import sys
import pandas

fp = open('graph_homework_notes.md')
sumb=0
count=0
uni=''
uni_grade = {}
for i in fp.readlines():
    try:
        if i.startswith('__'):
            uni=i.split(':')[0]
            uni=uni.replace('__',"")
            uni=uni.replace('\n',"")
        if i.startswith('score:'):
            a = i.split(':')[1].replace('\n',"").strip()
            print int(a)
            uni_grade[uni]= int(a)+25
    except:
        pass

grades=pandas.DataFrame.from_dict(uni_grade,orient='index')
grades.to_csv("cw_grades.csv",header=['grade'],index_label=['uni'])
# for (key,value) in uni_grade.iteritems():
#
#     grades['Vector vs. List (60619)'][key]=value
# grades.to_csv('vector_vs_list.csv')
