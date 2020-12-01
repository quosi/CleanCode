#!/usr/bin/env python3
import re
import glob
import pandas as pd
import numpy as np

class IqaLoggingProcessor:
    '''A tool to process logfiles of different IQA tools for image quality assesment 
    into a pandas dataframe. The IqaLoggingProcessor needs an absolut filepath 
    as input and will check for certain logfiles at this location.'''
    
    def __init__(self, inpath):
        self.inpath = inpath
        
    # implement functionality
    def getSubPathList(self):
        subdirlist = glob.glob(self.inpath + "/**/")
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
            exit(1)
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
        regex1 = r"^\s+\d+\s\d+\.\d+\s\d+\.\d+"
        regex2 = r"(?P<index>sm\s+)(?P<value>\d+\.\d+)"
        readLog = open(filepath + filename)
        for line in readLog:
            valuesFound = re.findall(regex1, line)
            smDeltaEFound = re.findall(regex2, line)
            [values.append(value) for value in valuesFound if len(value) > 0]
            [smDeltaE.append(float(sm[1])) for sm in smDeltaEFound if len(smDeltaEFound) > 0]
        readLog.close()
        for v in values:
            frame, mean, max_ = v.split()
            frames.append(int(frame))
            meanDeltaE.append(float(mean))
            maxDeltaE.append(float(max_))
        try:
            #print(len(smDeltaE))
            smDeltaE.pop(-1)
        except:
            print("Error Id1 --> Logfile " + filename + " incomplete!")
            exit(1)
        if len(frames) == len(meanDeltaE) == len(maxDeltaE) == len(smDeltaE):
            print("Reading   --> " + filename)
            return [frames, meanDeltaE, maxDeltaE, smDeltaE]
        else:
            print("Error Id2 --> Logfile " + filename + " incomplete!")
            print(f'Detected  --> {len(frames)} Frames, {len(meanDeltaE)} mean dE, {len(maxDeltaE)} max dE, {len(smDeltaE)} sm dE')
            exit(1)

    def getIctcpValues(self, filepath, filename):
        frames = []
        maxDeltaE = []
        aveDeltaE = []
        regex1 = r"frame "
        regex3 = r" max "
        regex4 = r" ave "
        readLog = open(filepath + filename)
        for line in readLog:
            frameFound = re.findall(r"(?<={})\d+".format(regex1), line)
            maxDeltaEFound = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(regex3), line)
            aveDeltaEFound = re.findall(r"(?<={})\d+\.\d+\D+?\d+".format(regex4), line)
            [frames.append(int(f)) for f in frameFound if len(frameFound) > 0]
            [maxDeltaE.append(float(maxd)) for maxd in maxDeltaEFound if len(maxDeltaEFound) > 0]
            [aveDeltaE.append(float(ave)) for ave in aveDeltaEFound if len(aveDeltaEFound) > 0]
        readLog.close()
        if len(frames) == len(maxDeltaE) == len(aveDeltaE):
            print("Reading --> " + filename)
            return [frames, maxDeltaE, aveDeltaE]
        else:
            print("Error Id3   --> Logfile " + filename + " incomplete!")
            exit(1)

    def createDataframe(self, filepath, filename, nameComponents):
        metric, _, _, _, _, _, _, _ = [*nameComponents]
        if metric == "ictcp":
            columnames = ['Frame', 'Delta ICTCP max', 'Delta ICTCP ave']
            data = self.getIctcpValues(filepath, filename)
        elif metric == "dE2000":
            columnames = ['Frame', 'DeltaE CIE2000 mean', 'DeltaE CIE2000 max', 'smoothed DeltaE CIE2000']
            data = self.getDeltaE2000Values(filepath, filename)
        else:
            print(f"Error Id4  --> Unsupportet metric: {metric}. Please check log file name string.")
            exit(1)
        content = list(zip(*data))
        df = pd.DataFrame(list(np.array(content)), columns=columnames)
        return df