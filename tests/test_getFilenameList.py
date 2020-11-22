import pytest
from src.IqaLoggingProcessor import IqaLoggingProcessor as iqa

inpath = ['/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/dE2000/']
fileList = ['dE2000_out_dm3_t49_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm3_t27_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm4_t49_BER-SUN_no-opt_win.txt', 
    'dE2000_out_dm3_t49_BER-SUN_no-opt_win.txt', 
    'dE2000_out_dm3_t1_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm4_t49_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm4_t27_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm4_t1_BER-SUN_opt-avx2_win.txt', 
    'dE2000_out_dm4_t27_BER-SUN_no-opt_win.txt', 
    'dE2000_out_dm4_t1_BER-SUN_no-opt_win.txt', 
    'dE2000_out_dm3_t1_BER-SUN_no-opt_win.txt', 
    'dE2000_out_dm3_t27_BER-SUN_no-opt_win.txt']

def test_getFilenameList():
    iqaProcessor = iqa(inpath)
    pathList = iqaProcessor.getSubPathList()
    files = iqaProcessor.getFilenameList(pathList[0])
    assert files == fileList