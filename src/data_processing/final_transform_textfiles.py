#########################################################################################################################################
## Project: ADHD NLP
## Script Name: transform_textfiles.py
## Script purpose: Convert text files to pandas dataframe
## Date: 8/18/20
## Author: Santosh
#########################################################################################################################################

import pandas as pd
import numpy as np
import os
import csv
import re

#---------------------------Transverse Original Text File Folder and Import Text Files as DF---------------------------#
def extractOriginalText(input_path):
    results = [(f,os.path.join(dp, f)) for dp, dn, filenames in os.walk(input_path) for f in filenames if os.path.splitext(f)[1] == '.txt']
    rows = []
    for i in range(len(results)):
        row = pd.read_csv(results[i][1], sep="\t", quoting=csv.QUOTE_NONE).iloc[:, [6]]
        row.columns = ['note_des']
        row['file'] = results[i][0]
        rows.append(row)
    return pd.concat(rows)


#---------------------------Transverse Annotated XMI Files and Create DF-----------------------------------------------#
def extractXMIAnnotation(input_path):
    # %% Write Patterns
    id_match = re.compile("(?<=xmi:id=\")\d{,5}(?=\")")
    begin_match = re.compile("(?<=begin=\")\d{,6}(?=\")")
    end_match = re.compile("(?<=end=\")\d{,6}(?=\")")
    tag_match = re.compile("(?<=semanticTag=\")\w*(?=\")")

    results = [(f.replace(".xmi",".txt"),os.path.join(dp, f)) for dp, dn, filenames in os.walk(input_path) for f in filenames if os.path.splitext(f)[1] == '.xmi']
    rows = []
    for i in range(len(results)):
        file = open(results[i][1], "r+")
        lines = file.readlines()
        lines = lines[0].split('><')
        extract = [x for x in lines if re.search("semanticTag", x)]
        extract = [(id_match.findall(x),
                    begin_match.findall(x),
                    end_match.findall(x),
                    tag_match.findall(x))
                   for x in extract]
        unique_tags = sorted(list(set([x[3][0] for x in extract])))
        file_name = re.findall("\\A.*(?=\.)",os.path.basename(results[i][0]))[0].split("-")

        row = pd.DataFrame({'xmi': [results[i][1]],
                            'file': [results[i][0]],
                            'anon_id': [file_name[1]],
                            'encounter_id': [file_name[2]]})

        for tag in unique_tags:
            row.loc[:, tag] = 1

        rows.append(row)

    full = pd.concat(rows).fillna(0)

    full['weak_bt'] = np.where((full['Counsel_Handout_BT'] == 1) |
                               (full['Counsel_Parent_BT'] == 1), 1, 0)

    full['strong_bt'] = np.where((full['Refer_Parent_BT'] == 1) |
                                 (full['Refer_School_BT'] == 1), 1, 0)

    full['bt_yn'] = np.where((full['weak_bt'] == 1) |
                             (full['strong_bt'] == 1), 1, 0)

    return full

