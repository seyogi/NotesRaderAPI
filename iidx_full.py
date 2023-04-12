import numpy as np
import csv
import os
import sys
import pprint
import pandas as pd


def create_dict(csv_sph,csv_spa,csv_spl):
    dict = {}
    csv_header = ['曲名','NOTES','PEAK','SCRATCH','SOF-LAN','CHARGE','CHORD','ノート数']
    dict_sph = csv.DictReader(csv_sph, csv_header)
    dict_spa = csv.DictReader(csv_spa, csv_header)
    dict_spl = csv.DictReader(csv_spl, csv_header)
    for row in dict_sph:
        dict[row['曲名']] = {'sph':row}
    for row in dict_spa:
        dict[row['曲名']] |= {'spa':row}
    for row in dict_spl:
        dict[row['曲名']] |= {'spl':row}
    return dict

def calc_score(dict,name,diff,score,Theme):
    if name in dict:
        if diff in dict[name]:
            if float(dict[name][diff]['ノート数']) != 0:
                MAX_score = float(dict[name][diff]['ノート数']) * 2
                per_score = score / MAX_score
                return round(float(dict[name][diff][Theme]) * per_score,2)
    return 0

def f(file_path,Theme):
    csv_file = open(file_path, "r", encoding="utf-8", errors="", newline="" )
    f = pd.read_csv(csv_file)
    csv_file.close()
    list_score = f[['タイトル', 'HYPER スコア', 'ANOTHER スコア', 'LEGGENDARIA スコア']].values.tolist()

    csv_sph = open("resources/Hyper.csv", "r", encoding="utf-8", errors="", newline="" )
    csv_spa = open("resources/Another.csv", "r", encoding="utf-8", errors="", newline="" )
    csv_spl = open("resources/Leggendaria.csv", "r", encoding="utf-8", errors="", newline="" )
    dict = create_dict(csv_sph,csv_spa,csv_spl)
    csv_sph.close()
    csv_spa.close()
    csv_spl.close()

    dict_score = []
    for score in list_score:
        dict_score.append({'曲名':score[0],'sph':score[1],'spa':score[2],'spl':score[3]})

    que_score = [[0]]

    for row in dict_score:
        for diff in ['sph','spa','spl']:
            S = calc_score(dict,row['曲名'],diff,float(row[diff]),Theme)
            if S > que_score[-1][0]:
                que_score.append([S,row['曲名'],diff])
                que_score = sorted(que_score, reverse=True)
            if len(que_score)>10:
                que_score.pop()
    
    #pprint.pprint(que_score)

    return que_score

def main():
    args = sys.argv
    if len(args) != 3:
        print("args error")
        return
    f(args[1],args[2])

if __name__ == "__main__":
    main()