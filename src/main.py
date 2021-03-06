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
        if len(opts) < 1:
            print('USAGE --> python3 main.py -i <inpath> -o <outpath>')
            print('INFO  --> Please use -h option for help.')
            sys.exit(1)
    except getopt.GetoptError:
        print('USAGE --> python3 main.py -i <inpath> -o <outpath>')
        print('INFO  --> Please use -h option for help.')
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print('USAGE --> python3 main.py -i <inpath> -o <outpath>')
            print('INFO  --> Supported IQA tools: ictcp_tool, dE2000')
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
        outDir = outpath + pathId[i] + "/"
        print(f"Enter   --> {pathId[i]}")
        try:
            os.mkdir(outDir)
        except OSError as error:
            print(error)
        for file in files:
            fileComponents = iqaProcessor.getFilenameComponents(file)
            data = iqaProcessor.createDataframe(path, file, fileComponents)
            plotter = IqaPlotter(data, outDir, fileComponents, file)
            df = plotter.prepareDataFrame()
            plotter.getInteractivePlot(df)
            plotter.getSimplePlot(df)

# 3. executing main function
if __name__ == "__main__":
    main(sys.argv[1:])
exit(0)