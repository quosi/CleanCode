import re
import glob

class IqaLoggingProcessor:
    '''A tool to process logfiles of different IQA tools for image quality assesment into a pandas dataframe.
    The IqaLoggingProcessor needs an absolut filepath as input and will check for certain logfiles at this location.'''
    def __init__(self, inpath):
        self.inpath = inpath
        
    # implement functionality

    def getFilenameList(self):
        pass
        #return filenamelist

    def getFilepathList(self):
        mainContent = glob.glob(self.inpath + "**/")
        print(mainContent)
        absolutSubdirs = [dirpath.split("/") for dirpath in mainContent]
        print(absolutSubdirs)
        return absolutSubdirs
        #return filepathlist

    def get_filename_components(self, filename):
        frase = r"(?<=dE2000_out_).+(?=_)"
        match = re.findall(frase, filename)
        algo, target, tools, opt = match[0].split("_")
        tools = tools.split("-")
        return algo, target, tools[0], tools[1], opt

iqa = IqaLoggingProcessor("/Users/hquos/Projects/DSV_libdm4/logs/01_DvDmApp/ictcp/")
iqa.getFilepathList()