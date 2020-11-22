import pytest
from src.IqaLoggingProcessor import IqaLoggingProcessor as iqa

inpath = ['/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/dE2000/']
subIdList = ["030", "092541000", "092541003", "092541010", "092541013"]

def test_getSubPathId():
    iqaProcessor = iqa(inpath)
    pathList = iqaProcessor.getSubPathList()
    assert pathList == subIdList