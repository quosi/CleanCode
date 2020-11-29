import os
import sys
import pandas as pd

import pytest
from src.IqaPlotter import IqaPlotter as ip

df = pd.DataFrame([[0, '1.4','0.6'],[1, '0.3', '0.0'],[2, '0.8','0.1']], columns=['Frame', 'Delta ICTCP max', 'Delta ICTCP ave'])
outpath = "out/plot/"
namecomponents = ["metric", "size", "algo", "target", "tool1", "tool2", "opt", "os"]
filename = "test.txt"

def test_always_passes():
    assert True

def test_always_fails():
    assert False

def test_IqaPlotter():
    assert ip(df, outpath, namecomponents, filename)