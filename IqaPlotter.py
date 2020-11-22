#!/usr/bin/env python3
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import Range1d
from bokeh.embed import components
#from IqaLoggingProcessor import IqaLoggingProcessor

class IqaPlotter:
    '''A tool to plot IQA data that was pre-processed by 
    the IqaLoggingProcessor module.'''
    
    def __init__(self, df, outpath, namecomponents, filename):
        self.df = df
        self.file = filename.split('.')[0]
        self.outpath = outpath
        self.metric, self.size, self.algo, self.target, self.tool1, self.tool2, self.opt, self.os = [*namecomponents] 
        self.targetDict = {'t1': '100', 't27': '600', 't49': '1000'}
        if self.metric == "ictcp":
            self.threshold = {'min': 0.2, 'max': 1, 'yAxis': 2}
        else:
            self.threshold = {'min': 1, 'max': 2.5, 'yAxis': 3}

    # implement functionality
    def prepareDataFrame(self):
        '''The external ictcp_tool metric returns separat values 
        for luma & chroma analysis when option -x was activated. 
        This function checks for its activation and separates 
        luma and chroma data in separat DataFrames columns.'''
        if int(self.df.iloc[-1][0]) != int(self.df.index[-1]):
            lumaColumns = [c + " Luma" for c in list(self.df.columns)]
            chromaColumns = [c + " Chroma" for c in list(self.df.columns)]
            dfLuma = pd.DataFrame(columns=lumaColumns)
            dfChroma = pd.DataFrame(columns=chromaColumns)
            for i in range(int(self.df.index[-1])+1):
                if i%2 == 0:
                    dfLuma = dfLuma.append(pd.Series(list(self.df.iloc[i]), index=lumaColumns), ignore_index=True)
                else:
                    dfChroma = dfChroma.append(pd.Series(list(self.df.iloc[i]), index=chromaColumns), ignore_index=True)
            combinedDataFrame = pd.concat([dfLuma[lumaColumns], dfChroma[chromaColumns[1:]]], axis = 1)
            #print("---------> Splitting Luma and Chroma data")
            return combinedDataFrame
        else:
            return self.df

    def getSimplePlot(self, dataFrame):
        '''Creates a <filename>.png plot visulizing IQA results from  
        the pre-processed DataFrame and saves it to the mentioned <IqaPlotter.outpath>'''
        color = {0: 'b.', 1: 'c.', 2: 'y.', 3: 'k.'}
        frames = int(dataFrame.iloc[-1][0])+1
        x = range(frames)
        plt.figure(figsize=(10, 6))
        for i, column in enumerate(list(dataFrame.columns)[1:]):
            plt.plot(x, dataFrame[column].astype(float), color[i], label = column)
        plt.plot(x, [self.threshold["min"],]*frames, 'g', label = f'Threshold of {self.threshold["min"]} JND', linestyle='dotted')
        plt.plot(x, [self.threshold["max"],]*frames, 'r', label = f'Threshold of {self.threshold["max"]} JND', linestyle='dotted')
        maxYticks = math.ceil(max(dataFrame[list(dataFrame.columns)[1:]].max()))
        if maxYticks < self.threshold['yAxis']:
            maxYticks = self.threshold['yAxis']
        plt.yticks(range(0, maxYticks, math.ceil(maxYticks/10)))
        plt.xticks(range(0, int(math.ceil(frames/10))*10+1, 20))
        plt.xlabel('number of frames')
        plt.ylabel(f'DeltaE {self.metric} error level')
        plt.title(f'Target {self.target[1:]} - {self.targetDict[self.target]}nits image quality comparison of {self.tool1} {self.opt} vs. {self.tool2} {str.upper(self.algo)} module')
        plt.legend()
        plt.savefig(self.outpath + self.file + ".png", dpi=200)

    def getInteractivePlot(self, dataFrame):
        output_file(self.outpath + self.file + ".html")
        tools = ["pan","box_zoom","hover","reset","save"]
        tooltips = [("Frame", "$index"),("JND", "$y")]
        maxYticks = math.ceil(max(dataFrame[list(dataFrame.columns)[1:]].max()))
        if maxYticks < self.threshold['yAxis']:
            maxYticks = self.threshold['yAxis']
        color = {0: 'lightseagreen', 1: 'orchid', 2: 'deepskyblue', 3: 'orange', 4: 'olive'}
        frames = int(dataFrame.iloc[-1][0])+1
        x = range(frames)
        plot = figure(tools=tools, tooltips=tooltips, toolbar_location="above", y_range = [0, maxYticks], 
            title=f'Target {self.target[1:]} - {self.targetDict[self.target]}nits image quality comparison of {self.tool1} {self.opt} vs. {self.tool2} {str.upper(self.algo)} module',
            x_axis_label='Number of frames', y_axis_label=f'DeltaE {self.metric} error level in JND', plot_width=1000, plot_height=500)
        for i, column in enumerate(list(dataFrame.columns)[1:]):
            plot.line(x, dataFrame[column].astype(float), legend_label=column, line_color=color[i])
            plot.circle(x, dataFrame[column].astype(float), legend_label=column, fill_color="white", fill_alpha=0.4, line_color=color[i], size=8)
        plot.line(x, [self.threshold["min"],]*frames, legend_label=f'Threshold of {self.threshold["min"]} JND', line_color="yellowgreen", line_dash="4 4", line_width=2, alpha=0.5)
        plot.line(x, [self.threshold["max"],]*frames, legend_label=f'Threshold of {self.threshold["max"]} JND', line_color="red", line_dash="4 4", line_width=2, alpha=0.5)
        save(plot)