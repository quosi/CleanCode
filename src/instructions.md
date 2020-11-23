# User Instructions

Please find here information about the usage of the IQA Analyzer module, its capabilities and requirements to run it successfully.

## Requirements

* Python 3
* conda environment (or you favorite virtual env)
* Python modules from ```src/requirements.txt```:
  + numpy1
  + pandas
  + matplotlib
  + bokeh
  + glob2
  + pytest
  
 Tested on:
 
 Software | Version
 ---------|---------
 MacOS    | Cataline 10.15.7 
 ---------|---------
 Python   | 3.7.6
 ---------|---------
 pip      | 20.0.2
 ---------|---------
 pytest   | 5.3.5
 
  
 ## Simple Setup Instructions
 
- [ ] Setup your virtual environment (recommended: conda environment)
- [ ] Install Python and pip 
- [ ] Install required python packages with pip installer
  ```$ pip install -r requirements.txt```
- [ ] Start ```src/main.py``` python script with required command line arguments for:
 * main directory path of your IAQ log files 
    + ```-i /User/ada/...log/ictcp/
 * main output path for your plot files 
    + ```-o /User/ada/...plots/

 
