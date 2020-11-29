import pytest
from src.IqaLoggingProcessor import IqaLoggingProcessor as iqa

inpath = ['/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/dE2000/']
filename = "ictcp_out_dm3_t27_BER-SUN_opt-avx2_win.txt"
components = ["ictcp", "out", "dm3", "t27", "BER", "SUN", "opt-avx2", "win"]

def test_getFilenameComponents():
    iqaProcessor = iqa(inpath)
    assert components == iqaProcessor.getFilenameComponents(filename)