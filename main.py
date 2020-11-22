import sys
import os
import getopt
from IqaLoggingProcessor import IqaLoggingProcessor
from IqaPlotter import IqaPlotter

def main(argv):
    '''This module processes <logfiles.txt> of different 
    image quality assesment(IQA) tools and
    provides a visual analysis of there results.'''

    # 1. catch command line input arguments
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["inpath=", "outpath="])
    except getopt.GetoptError:
        print('python3 main.py -i <inpath> -o <outpath>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('python3 main.py -i <inpath> -o <outpath>')
            print('Supported IQA tools: \n - ictcp_tool\n - dE2000')
            sys.exit(0)
        elif opt in ("-i", "--inpath"):
            inpath = arg
        elif opt in ("-o", "--outpath"):
            outpath = arg
        else:
            print("Unsupported argument. \n Please use -h option for help.")

    # 2. Data retrieval and processing
    iqaProcessor = IqaLoggingProcessor(inpath)
    pathList = iqaProcessor.getSubPathList()
    pathId = iqaProcessor.getSubPathId(pathList)
    for i, path in enumerate(pathList):
        files = iqaProcessor.getFilenameList(path)
        outDir = outpath + pathId[i]
        try:
            os.mkdir(outDir)
        except OSError as error:
            print(error)
        for file in files:
            fileComponents = iqaProcessor.getFilenameComponents(file)
            ictcpData = iqaProcessor.getIctcpValues(path, file)
            data = iqaProcessor.createDataframe(ictcpData, fileComponents)
            plotter = IqaPlotter(data, outDir, fileComponents, file)
            df = plotter.prepareDataFrame()
            plotter.getInteractivePlot(df)
            plotter.getSimplePlot(df)

# 3. executing main function
if __name__ == "__main__":
    main(sys.argv[1:])
exit(0)