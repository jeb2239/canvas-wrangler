# %%

from canvas_wrangler.canvasAPI import CanvasAPI
import numpy as np
import pandas as pd
import zipfile as zf
import os
import json
import csv
import shutil as sh
import markdown



def id_uni_converters(gradeSheet_df):
    sis_id = "SIS Login ID"
    gradeSheet_df=gradeSheet_df[pd.notnull(gradeSheet_df[sis_id])]
    gradeSheet_df
    id_to_uni = {}
    uni_to_id = {}
    for row in gradeSheet_df.iterrows():
        # print row[1]["ID"]
        # print row[1][sis_id]
        id_to_uni[str(int(row[1]["ID"]))]=row[1][sis_id]
        uni_to_id[row[1][sis_id]] = row[1]["ID"]
    return id_to_uni,uni_to_id

cwjson=json.load(open("cw.json"))
gradeSheet_df = pd.DataFrame.from_csv(cwjson['grades'])
id_to_uni,uni_to_id = id_uni_converters(gradeSheet_df)
new_api = CanvasAPI()
pddf = pd.DataFrame.from_dict(new_api.get_courses())
pddf['course_code']
pddf['id']
course_code_id=zip(pddf['course_code'],pddf['id'])
course_to_code_df = pd.DataFrame(columns=pddf['course_code'].values)
course_to_code_df.loc[0]=map(str,pddf['id'].tolist())



bjarne_hwk = new_api.get_assignments(course_to_code_df["COMSW4995_007_2017_1 - TOPICS IN COMPUTER SCIENCE"][0])[9]

bjarne_hwk


# %%
bjarne_hwk_df=pd.DataFrame(bjarne_hwk)
print bjarne_hwk_df
startpath = os.getcwd()
for root,dirs,files in os.walk(startpath):
    level = root.replace(startpath, '').count(os.sep)
    indent = ' ' * 4 * (level)
    current_dir=os.path.basename(root)
    if current_dir in cwjson["download"]:
        print '{}{}/'.format(indent,os.path.basename(root))
        subindent = ' '*4* (level+1)
        for f in files:
            try:
                abs_path = '{}/{}'.format(root,f)


                r=f.replace("_late","")
                ID=r.split("_")[1]
                print abs_path
                if zf.is_zipfile(abs_path):
                    # print "-is zipfile-"
                    try:
                        zipfile = zf.ZipFile(abs_path)
                        uni=id_to_uni[ID]
                        output_dir = "{}/{}".format(root,uni)
                        os.mkdir(output_dir)
                        zipfile.extractall(output_dir)

                    except:
                        pass

                else:
                    output_dir = "{}/{}".format(root,uni)
                    try:
                        uni=id_to_uni[ID]
                        output_dir = "{}/{}".format(root,uni)

                        os.mkdir(output_dir)
                        sh.copy(abs_path,output_dir)
                    except:
                        pass
                    # print "-is not zipfile-"
            except:
                pass


# %%
