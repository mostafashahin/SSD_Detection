import glob, os, subprocess
from os.path import normpath, splitext, join, isfile
def Get_Segnments_From_TextGrid_Short(TextGrid_File,Speaker='CHILD'):
    with open(TextGrid_File,'r') as fTextGrid:
        TextGrid_content = fTextGrid.read().splitlines()
    aSegments = [(TextGrid_content[i-2],TextGrid_content[i-1]) for i in range(len(TextGrid_content)) if TextGrid_content[i].find(Speaker)!=-1]
    return aSegments

def Select_Data(Dataset_Folder, TextGrid_Folder, Sessions='', Tasks=[]):
    #List All wavs in the Wave_Folder recercievely
    dWaves_Segments = {}
    lWave_Files = glob.glob(join(Dataset_Folder,'**','*[' + ''.join(Tasks) + '].wav'), recursive=True)
    #print(lWave_Files)
    for sWave_File in lWave_Files:
        if Sessions=='':
            sSpeakerID, sUttID = normpath(splitext(sWave_File)[0]).split(os.sep)[-2:]
            sTextGrid_Name = '-'.join([sSpeakerID, sUttID])+'.TextGrid'
            sTextGrid_File = join(TextGrid_Folder,sTextGrid_Name)
            if isfile(sTextGrid_File):
                dWaves_Segments[sWave_File] = Get_Segnments_From_TextGrid_Short(sTextGrid_File)
            else:
                print(sTextGrid_File)
            #lWavs_TextGrids.append((sWave_File,os.path.join(TextGrid_Folder,sTextGrid_Name)))
        else:
            sSpeakerID, sSessionID, sUttID = os.path.normpath(splitext(sWave_File)[0]).split(os.sep)[-3:]
            if sSessionID in Sessions:
                sTextGrid_Name = '-'.join([sSpeakerID, sSessionID, sUttID])+'.TextGrid'
                sTextGrid_File = join(TextGrid_Folder,sTextGrid_Name)
                if isfile(sTextGrid_File):
                    dWaves_Segments[sWave_File] = Get_Segnments_From_TextGrid_Short(sTextGrid_File)
                else:
                    print(sTextGrid_File)
                #lWavs_TextGrids.append((sWave_File,os.path.join(TextGrid_Folder,sTextGrid_Name)))
    return dWaves_Segments

def Write_Wave_Segments_To_File(dWaves_Segments,sOutput_File):
    with open(sOutput_File,'w') as fOutput_File:
        for sWave_File in dWaves_Segments:
            for tSegment in dWaves_Segments[sWave_File]:
                print(';'.join([sWave_File] + [str(i) for i in tSegment]), file = fOutput_File)
    return


def Extract_Features_openSmile(sWave_Segments_File, sConfig_File='../openSmile/config/gemaps/GeMAPSv01a.conf', sSegment_Level_csv_File='output_GeMAPs.csv', sFram_Level_csv_File=''):
    with open(sWave_Segments_File) as fSegments:
        for sLine in fSegments:
            sWave_File, sStart, sEnd = sLine.split(';')
            command = ['../openSmile/bin/SMILExtract','-C',sConfig_File,'-I',sWave_File,'-start',sStart,'-end',sEnd,'-instname',sWave_File,'-csvoutput',sSegment_Level_csv_File]
            subprocess.run(command)
    return



