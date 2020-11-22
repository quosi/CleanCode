#!/usr/bin/env python3
import re
import glob
import pandas as pd
import numpy as np

class IqaLoggingProcessor:
    '''A tool to process logfiles of different IQA tools for image quality assesment into a pandas dataframe.
    The IqaLoggingProcessor needs an absolut filepath as input and will check for certain logfiles at this location.'''
    def __init__(self, inpath):
        self.inpath = inpath
        
    # implement functionality
    def getSubPathList(self):
        subdirlist = glob.glob(self.inpath + "**/")
        return subdirlist

    def getFilenameList(self, path):
        filepath = glob.glob(path + "/*.txt")
        filenamelist = [filelocation.split("/")[-1] for filelocation in filepath]
        return filenamelist

    def getFilenameComponents(self, filename):
        components = filename.split("_")
        if len(components) == 7:
            metric, size, algo, target, tools, opt, os = [*components]
            tools = tools.split("-")
            os = os.split(".")[0]
        else:
            print(f"--> Unsupportet IQA log file type: {filename}")
        return metric, size, algo, target, tools[0], tools[1], opt, os

    def getSubPathId(self, subPath):
        pathId = [p.split('/')[-2] for p in subPath]
        return pathId

    def getDeltaE2000Values(self, filepath, filename):
        values = []
        frames = []
        meanDeltaE = []
        maxDeltaE = []
        # sm uses a smoothening filter size 11, sigma 3
        smDeltaE = []
        # define regular expressions to find values in log file
        regex1 = r"^\s+\d+\s\d+\.\d+\s\d+\.\d+"
        regex2 = r"(?P<index>sm\s+)(?P<value>\d+\.\d+)"
        readLog = open(filepath + filename)
        for line in readLog:
            valuesFound = re.findall(regex1, line)
            smDeltaEFound = re.findall(regex2, line)
            [values.append(value) for value in valuesFound if len(value) > 0]
            [smDeltaE.append(sm[1]) for sm in smDeltaEFound if len(smDeltaEFound) > 0]
        readLog.close()
        for v in values:
            frame, mean, max_ = v.split()
            frames.append(frame)
            meanDeltaE.append(mean)
            maxDeltaE.append(max_)
        smDeltaE.pop(-1)
        if len(frame) == len(meanDeltaE) == len(maxDeltaE) == len(smDeltaE):
            print("Reading --> " + filename)
            return [frames, meanDeltaE, maxDeltaE, smDeltaE]
        else:
            print("Date extraction not possible! \n Please check log file for completeness or format.")
            return None

    def getIctcpValues(self, filepath, filename):
        frames = []
        #minDeltaE = []
        maxDeltaE = []
        aveDeltaE = []
        regex1 = r"frame "
        #regex2 = r"\{ min "
        regex3 = r" max "
        regex4 = r" ave "
        readLog = open(filepath + filename)
        for line in readLog:
            frameFound = re.findall(r"(?<={})\d+".format(regex1), line)
            #minDeltaEFound = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(regex2), line)
            maxDeltaEFound = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(regex3), line)
            aveDeltaEFound = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(regex4), line)
            [frames.append(f) for f in frameFound if len(frameFound) > 0]
            #[minDeltaE.append(mind) for mind in minDeltaEFound if len(minDeltaEFound) > 0]
            [maxDeltaE.append(maxd) for maxd in maxDeltaEFound if len(maxDeltaEFound) > 0]
            [aveDeltaE.append(ave) for ave in aveDeltaEFound if len(aveDeltaEFound) > 0]
        readLog.close()
        #if len(frames) == len(minDeltaE) == len(maxDeltaE) == len(aveDeltaE):
        if len(frames) == len(maxDeltaE) == len(aveDeltaE):
            print("Reading --> " + filename)
            #return [frames, minDeltaE, maxDeltaE, aveDeltaE]
            return [frames, maxDeltaE, aveDeltaE]
        else:
            print("Date extraction not possible! \n Please check log file for completeness or format.")
            return None

    def createDataframe(self, data, nameComponents):
        metric, _, _, _, _, _, _, _ = [*nameComponents]
        if metric == "ictcp":
            # create ictcp index for df
            columnames = ['Frame', #'Delta ICTCP min',
            'Delta ICTCP max', 'Delta ICTCP ave']
        elif metric == "dE2000":
            # create dE2000 index for df
            columnames = ['Frame', 'DeltaE CIE2000 mean', 
            'DeltaE CIE2000 max', 'smoothed DeltaE CIE2000']
        else:
            print("Unsupportet metric. \n Please check log file name string.")
        # create data frame from extraxted data
        content = list(zip(*data))
        df = pd.DataFrame(list(np.array(content)), columns=columnames)
        return df