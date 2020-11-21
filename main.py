import sys
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
    
    iqa = IqaLoggingProcessor(inpath)
    pathList = iqa.getSubPathList()
    files = iqa.getFilenameList(pathList[1])
    fileComponents = iqa.getFilenameComponents(files[1])
    ictcpData = iqa.getIctcpValues(pathList[1], files[1])
    df = iqa.createDataframe(ictcpData, fileComponents)
    print(df)

# -1. executing main function

if __name__ == "__main__":
    main(sys.argv[1:])

exit(0)