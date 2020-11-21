#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from IqaLoggingProcessor import IqaLoggingProcessor

class IqaPlotter:
    '''A tool to plot IQA data that was pre-processed by 
    the IqaLoggingProcessor module.'''
    
    def __init__(self, dataframe, outpath, namecomponents, filename):
        self.df = dataframe
        self.file = filename
        self.outpath = outpath
        self.metric, self.size, self.algo, self.target, self.tool1, self.tool2, self.opt, self.os = [*namecomponents] 

    # implement functionality
    def splittDf(self):
        '''The external ictcp_tool metric returns separat values 
        for luma & chroma analysis when option -x was activated. 
        This function checks for its activation and separates 
        luma and chroma data in separat DataFrames.'''

        # ----------------------------------------------------------------------
        # TODO need to get Luma and Chroma Values in separat COLUMNS not DFs!!
        # ----------------------------------------------------------------------

        if self.df.iloc[-1][0] != self.df.index[-1]:
            luma = []
            chroma = []
            for i in range(int(df.iloc[-1][0])+1):
                if i%2 == 0:
                    luma.append(i)
                else:
                    chroma.append(i)
            dfLuma = df.iloc[luma]
            dfChroma = df.iloc[chroma]
            print("Splitting Luma and Chroma data")
            return [dfLuma, dfChroma]
        else:
            return [df]

    def prepIctcpPlot(self):
        dataFrames = self.splittDf()
        pass

    def prepDeltaE2000Plot(self):
        pass

    def getSimplePlot(self, df):
        # for one df only ----> check TODO in line 25
        l_dict = {'t1': '100', 't27': '600', 't49': '1000'}
        color = {0: 'b.', 1: 'c.', 2: 'y.', 3: 'k.'}
        if self.metric == "ictcp":
            treshold = {'min': 0.2, 'max': 1, 'yAxis': 2}
        else:
            treshold = {'min': 1, 'max': 2.5, 'yAxis': 3}

        frames = int(df.index[-1])
        x = range(frames)
        plt.figure(figsize=(10, 6))
        for i, column in enumerate(list(df.columns)[1:]):
            plt.plot(x, df[column].astype(float), color[i], label = column)

        plt.plot(x, [treshold['min'],]*frames, 'g', label = f'Threshold of {treshold['min']} JND', linestyle='dotted')
        plt.plot(x, [treshold['max'],]*frames, 'r', label = f'Threshold of {treshold['max']} JND', linestyle='dotted')
        
        maxYticks = math.ceil(max(df[list(df.columns)[1:]].max()))
        if maxYticks < treshold['yAxis']:
            maxYticks = treshold['yAxis']

        plt.yticks(range(0, maxYticks, math.ceil(maxYticks/10)))
        plt.xticks(range(0, frames, 20))
        plt.xlabel('number of frames')
        plt.ylabel(f'DeltaE {self.metric} error level')
        title = f'Target {self.target[1:]} - {l_dict[self.target]}nits image quality comparison of {self.tool1} {self.opt} vs. {self.tool2} {str.upper(self.algo)} module'
        plt.title(title)
        plt.legend()
        plt.savefig(outpath + file.split('.')[0] + ".png", dpi=200)

    def getInteractivePlot(self):
        #use check-df function
        pass

# 2. Data retrieval and processing
inpath = "/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/ictcp/"
outpath = "/Users/hquos/Desktop/temp/"
iqa = IqaLoggingProcessor(inpath)
pathList = iqa.getSubPathList()
files = iqa.getFilenameList(pathList[0])
fileComponents = iqa.getFilenameComponents(files[2])
ictcpData = iqa.getIctcpValues(pathList[0], files[2])
df = iqa.createDataframe(ictcpData, fileComponents)
plot = IqaPlotter(df, outpath)
df1, df2 = plot.splittDf()
getSimplePlot(df2)