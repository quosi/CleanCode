#!/usr/bin/env python3
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

from IqaLoggingProcessor import IqaLoggingProcessor

class IqaPlotter:
    '''A tool to plot IQA data that was pre-processed by 
    the IqaLoggingProcessor module.'''
    
    def __init__(self, df, outpath, namecomponents, filename):
        self.df = df
        self.file = filename
        self.outpath = outpath
        self.metric, self.size, self.algo, self.target, self.tool1, self.tool2, self.opt, self.os = [*namecomponents] 

    # implement functionality
    def prepareDataFrame(self):
        '''The external ictcp_tool metric returns separat values 
        for luma & chroma analysis when option -x was activated. 
        This function checks for its activation and separates 
        luma and chroma data in separat DataFrames.'''
        if self.df.iloc[-1][0] != self.df.index[-1]:
            lumaColumns = [c + " Luma" for c in list(self.df.columns)]
            chromaColumns = [c + " Chroma" for c in list(self.df.columns)]
            dfLuma = pd.DataFrame(columns=lumaColumns)
            dfChroma = pd.DataFrame(columns=chromaColumns)
            for i in range(int(self.df.index[-1])+1):
                if i%2 == 0:
                    dfLuma = dfLuma.append(pd.Series(list(self.df.iloc[i]), index=lumaColumns), ignore_index=True)
                else:
                    dfChroma = dfChroma.append(pd.Series(list(self.df.iloc[i]), index=chromaColumns), ignore_index=True)
            combinedDataframe = pd.concat([dfLuma[lumaColumns], dfChroma[chromaColumns[1:]]], axis = 1)
            print("---> Splitting Luma and Chroma data")
            return combinedDataframe
        else:
            return self.df

    def getSimplePlot(self, dataFrame):
        # for one dataFrame only ----> check TODO in line 25
        l_dict = {'t1': '100', 't27': '600', 't49': '1000'}
        color = {0: 'b.', 1: 'c.', 2: 'y.', 3: 'k.'}
        if self.metric == "ictcp":
            threshold = {'min': 0.2, 'max': 1, 'yAxis': 2}
        else:
            threshold = {'min': 1, 'max': 2.5, 'yAxis': 3}
        frames = int(dataFrame.iloc[-1][0])+1
        x = range(frames)
        plt.figure(figsize=(10, 6))
        for i, column in enumerate(list(dataFrame.columns)[1:]):
            plt.plot(x, dataFrame[column].astype(float), color[i], label = column)
        plt.plot(x, [threshold["min"],]*frames, 'g', label = f'Threshold of {threshold["min"]} JND', linestyle='dotted')
        plt.plot(x, [threshold["max"],]*frames, 'r', label = f'Threshold of {threshold["max"]} JND', linestyle='dotted')
        maxYticks = math.ceil(max(dataFrame[list(dataFrame.columns)[1:]].max()))
        if maxYticks < threshold['yAxis']:
            maxYticks = threshold['yAxis']
        plt.yticks(range(0, maxYticks, math.ceil(maxYticks/10)))
        plt.xticks(range(0, int(math.ceil(frames/10))*10+1, 20))
        plt.xlabel('number of frames')
        plt.ylabel(f'DeltaE {self.metric} error level')
        plt.title(f'Target {self.target[1:]} - {l_dict[self.target]}nits image quality comparison of {self.tool1} {self.opt} vs. {self.tool2} {str.upper(self.algo)} module')
        plt.legend()
        plt.savefig(outpath + self.file.split('.')[0] + ".png", dpi=200)

    def getInteractivePlot(self):
        #use check-df function
        pass

# 2. Data retrieval and processing
inpath = "/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/ictcp/"
outpath = "/Users/hquos/Desktop/temp/"
iqa = IqaLoggingProcessor(inpath)
pathList = iqa.getSubPathList()
files = iqa.getFilenameList(pathList[0])
file = files[2]
fileComponents = iqa.getFilenameComponents(file)
ictcpData = iqa.getIctcpValues(pathList[0], file)
df_out = iqa.createDataframe(ictcpData, fileComponents)
plot = IqaPlotter(df_out, outpath, fileComponents, file)
df2 = plot.prepareDataFrame()
plot.getSimplePlot(df2)