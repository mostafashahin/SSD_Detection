from os.path import realpath, join, dirname, splitext, isfile
from subprocess import run
import numpy as np

def Get_Segments_From_VAD_CSV(sVADcsv):
    print('Parsing ',sVADcsv)
    aVAD = np.loadtxt(sVADcsv,delimiter=',')
    bEarlyStart = bLateEnd = False
    if aVAD[0,1] > 0:
        aVAD[0,1] = -1
        bEarlyStart = True
    if aVAD[-1,1] > 0:
        aVAD[-1,1] = -1
        #bLateEnd = True
    aConv = np.roll( np.sign(aVAD[:,1]), 1) - np.sign( aVAD[:,1])
    aStarts = aVAD[ np.where( aConv < 0 ), 0 ].flatten()
    aEnds = aVAD[ np.where( aConv > 0 ), 0 ].flatten()
    if bEarlyStart:
        aStarts = np.r_[aVAD[0,0],aStarts]
    if bLateEnd:
        aEnds = np.r_[aEnds,aVAD[-1,0]]
    assert aStarts.shape == aEnds.shape, "Mismatch in File %s Starts %d, Ends %d" % (sVADcsv,aStarts.shape[0], aEnds.shape[0])
    aSegments = [[fStart,fEnd,fEnd-fStart] for fStart,fEnd in zip(aStarts,aEnds)]
    return aSegments




def Select_Data_OGI(sDataDir, lAges = ['00','01','02','03','04','05','06','07','08','09','10'], bConvertWav = False, bVAD = False):
    dWaves_Segments = {}
    for sAge in lAges:
        with open(join(sDataDir,'docs',sAge+'-'+'verified.txt')) as fWavList:
            for sLine in fWavList:
                sWavFile, sValid = sLine.split()
                if sValid == '1':
                    sWavFile = join(realpath(sDataDir),sWavFile[3:])
                    sSpeakerID = sWavFile[-10:-7]
                    sWavFileHeader = splitext(sWavFile)[0]+'_h.wav'
                    sVADFile = splitext(sWavFile)[0]+'_vad.csv'
                    if bConvertWav and not isfile(sWavFileHeader):
                        print('Converting ',sWavFile)
                        command = ['sox',sWavFile,sWavFileHeader]
                        run(command)
                    if bVAD and not isfile(sVADFile):
                        print('Applying VAD ',sWavFile)
                        command = ['SMILExtract','-C','openSmile/config/vad/vad_opensource.conf','-I',sWavFileHeader,'-O',sVADFile]
                        run(command)
                    elif bVAD:
                        aSegments = Get_Segments_From_VAD_CSV(sVADFile)
                    dWaves_Segments[sWavFileHeader+sSpeakerID] = aSegments
                    #lValidData += [sWavFile] #if sValid == '1' else []
    return dWaves_Segments

