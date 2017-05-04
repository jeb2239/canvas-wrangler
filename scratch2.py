# %%
from canvas_wrangler.canvasAPI import CanvasAPI
import numpy as np
import pandas as pd
import zipfile as zf
import os
import json
import csv

cwjson=json.load(open("cw.json"))
gradeSheet_df = pd.DataFrame.from_csv(cwjson['grades'])
gradeSheet_dfcwjson=json.load(open("cw.json"))
gradeSheet_df = pd.DataFrame.from_csv(cwjson['grades'])

# %%
sis_id = "SIS Login ID"
gradeSheet_df=gradeSheet_df[pd.notnull(gradeSheet_df[sis_id])]
gradeSheet_df
#%%
id_to_uni = {}
uni_to_id = {}
for row in gradeSheet_df.iterrows():
    # print row[1]["ID"]
    # print row[1][sis_id]
    id_to_uni[str(int(row[1]["ID"]))]=row[1][sis_id]
    uni_to_id[row[1][sis_id]] = row[1]["ID"]
