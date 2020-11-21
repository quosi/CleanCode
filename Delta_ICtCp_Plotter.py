#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import random
import math
import os

def get_filename_components(filename):
    frase = r"(?<=ictcp_out_).+(?=_)"
    match = re.findall(frase, filename)
    algo, target, tools, opt = match[0].split("_")
    tools = tools.split("-")
    return algo, target, tools[0], tools[1], opt

def get_ictcp_values(filepath, filename):
    frame = []
    min_deltaE = []
    max_deltaE = []
    ave_deltaE = []
    gmax_deltaE = []
    gave_deltaE = []
    match1 = r"frame "
    match2 = r"\{ min "
    match3 = r" max "
    match4 = r" ave "
    match5 = r"Global average \= "
    match6 = r"maximum \= "
    
    read_log = open(filepath + filename)
    for txt_line in read_log:
        frame_found = re.findall(r"(?<={})\d+".format(match1), txt_line)
        min_deltaE_found = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(match2), txt_line)
        max_deltaE_found = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(match3), txt_line)
        ave_deltaE_found = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(match4), txt_line)
        gmax_deltaE_found = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(match5), txt_line)
        gave_deltaE_found = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(match6), txt_line)
        [frame.append(f) for f in frame_found if len(frame_found) > 0]
        [min_deltaE.append(mind) for mind in min_deltaE_found if len(min_deltaE_found) > 0]
        [max_deltaE.append(maxd) for maxd in max_deltaE_found if len(max_deltaE_found) > 0]
        [ave_deltaE.append(ave) for ave in ave_deltaE_found if len(ave_deltaE_found) > 0]
        [gmax_deltaE.append(gmax) for gmax in gmax_deltaE_found if len(gmax_deltaE_found) > 0]
        [gave_deltaE.append(gave) for gave in gave_deltaE_found if len(gave_deltaE_found) > 0]
    read_log.close()
    return frame, min_deltaE, max_deltaE, ave_deltaE, gmax_deltaE, gave_deltaE

# This function (draw_ictcp) contains the main functionality and calls the two previoues functions.
def draw_ictcp(file, inpath, outpath):
    algo, target, tools1, tools2, opt = get_filename_components(file)
    frame, min_deltaE, max_deltaE, ave_deltaE, gmax_deltaE, gave_deltaE = get_ictcp_values(inpath, file)
    name = "_".join((tools1, tools2, algo, target, opt))
    index = ['Source1', 'Source2', 'DM Algo', 'Target', 'Frame', 
             'Delta ICTCP min', 'Delta ICTCP max', 'Delta ICTCP ave',
             'Delta ICTCP Global max', 'Delta ICTCP Global average']
    content = []
    for f in range(0, len(frame), 1):
        temp = [tools1, tools2, algo, target, frame[f], 
                min_deltaE[f], max_deltaE[f], ave_deltaE[f], 
                gmax_deltaE[0], gave_deltaE[0]]
        content.append(temp)
        
    if len(frame) == len(min_deltaE) == len(max_deltaE) == len(ave_deltaE) and len(gmax_deltaE) == len(gave_deltaE) == 1:
        print("Reading --> " + name)
    else:
        print("Date extraction not possible! \n Please check log file format.")
    df = pd.DataFrame(list(np.array(content).T), index=index)
    luma = []
    chroma = []
    nr_frame = int((df.columns[-1]+1)/2)
    for i in range(df.columns[-1]+1):
        if i%2 == 0:
            luma.append(i)
        else:
            chroma.append(i)
            
    df_luma = df.iloc[:,luma]
    df_chroma = df.iloc[:,chroma]
    l_dict = {'t1': '100', 't27': '600', 't49': '1000'}
    
    x = range(len(df_luma.columns))
    show_value = 'Delta ICTCP max'
    y_l = [float(y) for y in df_luma.loc[show_value]]
    y_c = [float(y) for y in df_chroma.loc[show_value]]
    max_yticks = math.ceil(max(max(y_l), max(y_c)))
    if max_yticks < 2:
        max_yticks = 2
    plt.figure(figsize=(10, 6))
    plt.plot(x, y_l, label = "Luma " + show_value)
    plt.plot(x, y_c, label = "Chroma " + show_value)
    plt.plot(range(0,nr_frame), [0.2,]*nr_frame, label = 'Threshold of 0.2 JND')
    plt.plot(range(0,nr_frame), [1,]*nr_frame, label = 'Threshold of 1 JND')
    plt.yticks(range(0, max_yticks, math.ceil(max_yticks/10)))
    plt.xticks(range(0, 152, 20))
    plt.xlabel('number of frames')
    plt.ylabel('Delta ICTCP error level')
    plt.title(f'Target {target[1:]} - {l_dict[target]}nits image quality comparison of {tools1} {opt} vs. {tools2} {str.upper(algo)} modul')
    plt.legend()
    plt.savefig(outpath + file.split('.')[0] + ".png", dpi=200)

# prep files for processing
# enter path containing logfiles here:
mainpath = "/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/ictcp/"
main_content = glob.glob(mainpath + "**/")
subdirs = [dirpath.split("/") for dirpath in main_content]
cases = [subdir[-2] for subdir in subdirs]
cases_path = [mainpath+c for c in cases]

for case in cases_path:
    cases_content = glob.glob(case + "/*.*")
    full_paths = [p.split("/") for p in cases_content]
    files = [p.pop(-1) for p in full_paths]
    outpath = "/Users/hquos/Projects/DSV_libdm4/plots/" + case.split("/")[-1] + "/"
    try:
        os.mkdir(outpath) 
    except OSError as error: 
        print(error)
    print("Processing --> " + case.split("/")[-1])
    for file in files:
        draw_ictcp(file, case+"/", outpath)