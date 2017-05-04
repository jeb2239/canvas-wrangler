import pandas as pd
fp = open('graph_homework_notes.md','a')
csv = pd.read_csv('/home/barriosj/C++ Design/21_Mar_15-39_Grades-COMSW4995_007_2017_1.csv')
for i in csv['SIS Login ID']:
    if pd.isnull(i):
        continue
    
    fp.write('__'+str(i)+'__\n')
    fp.write("score:\n")
    fp.write("comments:\n\n")
    
    