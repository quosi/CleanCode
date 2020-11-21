#!/usr/bin/env python3
import pandas as pd
import numpy as np

class IqaPlotter:
    '''A tool to plott IQA data that was pre-processed by 
    the IqaLoggingProcessor module.'''
    
    def __init__(self, dataframe):
        self.df = dataframe
        
    # implement functionality
    def getSubPathList(self):

        # ATTENTION:
        # Size "UHD" activates luma-chroma-splitting for ictcp values in external IQA tool