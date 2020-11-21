#!/usr/bin/env python3
import pandas as pd
import numpy as np

class IqaPlotter:
    '''A tool to plot IQA data that was pre-processed by 
    the IqaLoggingProcessor module.'''
    
    def __init__(self, dataframe, outpath):
        self.df = dataframe
        self.outpath = outpath
        
    # implement functionality
    def getSimplePlot(self):
        return 0

    # ATTENTION:
    # Size "UHD" activates luma-chroma-splitting for ictcp values in external IQA tool