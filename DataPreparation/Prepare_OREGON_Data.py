from os.path import realpath, join, dirname

def Select_Data_OGI(sDataDir, lAges = ['00','01','02','03','04','05','06','07','08','09','10']):
    lValidData = []
    for sAge in lAges:
        with open(join(sDataDir,'docs',sAge+'-'+'verified.txt')) as fWavList:
            for sLine in fWavList:
                sWavFile, sValid = sLine.split()
                if sValid == '1':
                    sWavFile = join(realpath(sDataDir),sWavFile[3:])
                    lValidData += [sWavFile] #if sValid == '1' else []
    return lValidData

