import glob, os, subprocess
from os.path import normpath, splitext, join, isfile
import pandas as pd
import numpy as np
MAX_SAMPLES_NUMBER = 1000000
MIN_SEG_DUR = 0.5
def Get_Segnments_From_TextGrid_Short(TextGrid_File,Speaker='CHILD'):
    with open(TextGrid_File,'r') as fTextGrid:
        TextGrid_content = fTextGrid.read().splitlines()
    aSegments = [[float(TextGrid_content[i-2]),float(TextGrid_content[i-1]),float(TextGrid_content[i-1])-float(TextGrid_content[i-2])] for i in range(len(TextGrid_content)) if TextGrid_content[i].find(Speaker)!=-1]
    return aSegments

def Select_Data(Dataset_Folder, TextGrid_Folder, Sessions='', Tasks=[], bConvertTo16 = True):#, Train_Spkrs_List=[],Test_Spkrs_List=[]):
    #List All wavs in the Wave_Folder recercievely
    dWaves_Segments = {}
    #dWaves_Segments_Test  = {}
    lWave_Files = glob.glob(join(Dataset_Folder,'**','*[' + ''.join(Tasks) + '].wav'), recursive=True)
    #print(lWave_Files)
    for sWave_File in lWave_Files:
        if Sessions=='':
            sSpeakerID, sUttID = normpath(splitext(sWave_File)[0]).split(os.sep)[-2:]
            #if sSpeakerID in Train_Spkrs_List:
            #    dWaves_Segments = dWaves_Segments_Train
            #else:
            #    dWaves_Segments = dWaves_Segments_Test
            if bConvertTo16:
                print('Converting ',sWave_File)
                sWave_File_16 = splitext(sWave_File)[0]+'_16.wav'
                if not isfile(sWave_File_16):
                    command = ['sox',sWave_File,'-r','16000',sWave_File_16]
                    subprocess.run(command)

            sTextGrid_Name = '-'.join([sSpeakerID, sUttID])+'.TextGrid'
            sTextGrid_File = join(TextGrid_Folder,sTextGrid_Name)
            if isfile(sTextGrid_File):
                if bConvertTo16:
                    print('Converting ',sWave_File)
                    sWave_File_16 = splitext(sWave_File)[0]+'_16.wav'
                    if not isfile(sWave_File_16):
                        command = ['sox',sWave_File,'-r','16000',sWave_File_16]
                        subprocess.run(command)
                dWaves_Segments[sWave_File_16+sSpeakerID] = Get_Segnments_From_TextGrid_Short(sTextGrid_File)
            else:
                print(sTextGrid_File)
            #lWavs_TextGrids.append((sWave_File,os.path.join(TextGrid_Folder,sTextGrid_Name)))
        else:
            sSpeakerID, sSessionID, sUttID = os.path.normpath(splitext(sWave_File)[0]).split(os.sep)[-3:]
            #if sSpeakerID in Train_Spkrs_List:
            #    dWaves_Segments = dWaves_Segments_Train
            #else:
            #    dWaves_Segments = dWaves_Segments_Test
            if sSessionID in Sessions:
                sTextGrid_Name = '-'.join([sSpeakerID, sSessionID, sUttID])+'.TextGrid'
                sTextGrid_File = join(TextGrid_Folder,sTextGrid_Name)
                if isfile(sTextGrid_File):
                    if bConvertTo16:
                        print('Converting ',sWave_File)
                        sWave_File_16 = splitext(sWave_File)[0]+'_16.wav'
                        command = ['sox',sWave_File,'-r','16000',sWave_File_16]
                        subprocess.run(command)
                    dWaves_Segments[sWave_File_16+sSpeakerID] = Get_Segnments_From_TextGrid_Short(sTextGrid_File)
                else:
                    print(sTextGrid_File)
                #lWavs_TextGrids.append((sWave_File,os.path.join(TextGrid_Folder,sTextGrid_Name)))
    return dWaves_Segments #_Train, dWaves_Segments_Test

def Write_Wave_Segments_To_File(dWaves_Segments,sOutput_File):
    iExcSeg = iIncSeg = 0
    with open(sOutput_File,'w') as fOutput_File:
        for sWave_File in dWaves_Segments:
            for tSegment in dWaves_Segments[sWave_File]:
                fStart, fEnd,fDur = tSegment
                if fDur < MIN_SEG_DUR:
                    print(sWave_File,fStart, fEnd,fDur)
                    iExcSeg += 1
                else:
                    print(';'.join([sWave_File] + [str(i) for i in (fStart, fEnd)]), file = fOutput_File)
                    iIncSeg += 1
    return iExcSeg, iIncSeg

def Extract_Features_openSmile(sWave_Segments_File, sConfig_File='../openSmile/config/gemaps/GeMAPSv01a.conf', sSegment_Level_csv_File='output_GeMAPs.csv', sFram_Level_csv_File=''):
    with open(sWave_Segments_File) as fSegments:
        for sLine in fSegments:
            sWave_File_SpkID, sStart, sEnd = sLine.split(';')
            sWave_File = sWave_File_SpkID[:-3]
            print('Now Processing, ', sWave_File, ' From ', sStart, ' To ', sEnd )
            command = ['SMILExtract','-C',sConfig_File,'-I',sWave_File,'-start',sStart,'-end',sEnd,'-instname',sWave_File_SpkID,'-class','1','-csvoutput',sSegment_Level_csv_File]
            subprocess.run(command)
    return

def Split_Wavs_Train_Test_From_Speaker_List(aDataSets,sSplitFile,cv=False,nDim = 63):
    X_all = np.empty((MAX_SAMPLES_NUMBER,nDim),dtype=float)
    y_all = np.zeros((MAX_SAMPLES_NUMBER),dtype=int)
    aSpkrs_all = []
    iPnt = 0
    #Load sSplitFile
    pdSplitData = pd.read_csv(sSplitFile,sep=',')
    #aExcSpkrs = list(pdSplitData.loc[pdSplitData['Exclude']==1,'SpkID'])
    iNum_CV = pdSplitData['CV'].max()
    print(iNum_CV,MAX_SAMPLES_NUMBER/iNum_CV)
    iNum_Classes = pdSplitData['Class'].max()
    x = np.zeros(int((MAX_SAMPLES_NUMBER/iNum_CV)),dtype=int)
    aCV = []
    for i in range(iNum_CV):
        aCV.append([np.zeros(0,dtype=int),np.zeros(0,dtype=int)])
    for dataset in aDataSets:
        sDataset_Name, pdDataset_Data = dataset
        aDataset_Mask = pdSplitData['dataset'] == sDataset_Name
        X = pdDataset_Data.iloc[:,2:].values
        y = np.zeros(X.shape[0])
        aSpeakers = [ls[-4:-1] for ls in pdDataset_Data['name']]
        aSpkrs_all += [spkr+'_'+sDataset_Name for spkr in aSpeakers]
        aExcSpkrs = list(pdSplitData.loc[(pdSplitData['Exclude']==1) & aDataset_Mask,'SpkID'])
        #iNum_Classes = pdSplitData['Class'].max()
        for cls in range(1,iNum_Classes+1):
            aSpkrs = list(pdSplitData.loc[(pdSplitData['Class']==cls) & aDataset_Mask,'SpkID'])
            aSpkrs_indx = [i for i in range(len(aSpeakers)) if aSpeakers[i] in aSpkrs]
            print(sDataset_Name,cls,len(aSpkrs),len(aSpkrs_indx))
            y[aSpkrs_indx] = cls
        X_all[iPnt:iPnt+X.shape[0]] = X
        y_all[iPnt:iPnt+X.shape[0]] = y
        for iCV in range(iNum_CV):
            aSpkrs_cv = list(pdSplitData.loc[(pdSplitData['CV']==iCV+1) & aDataset_Mask,'SpkID'])
            print(sDataset_Name,iCV+1,aSpkrs_cv)
            aSpkrs_cv_indx = [i+iPnt for i in range(len(aSpeakers)) if (aSpeakers[i] in aSpkrs_cv and aSpeakers[i] not in aExcSpkrs)]
            aSpkrs_train_indx = [i+iPnt for i in range(len(aSpeakers)) if (aSpeakers[i] not in aSpkrs_cv and aSpeakers[i] not in aExcSpkrs)]
            #aSpkrs_train_indx = [i+iPnt for i in range(len(aSpeakers)) if i+iPnt not in aSpkrs_cv_indx]
            print(iCV+1,len(aSpkrs_cv_indx),len(aSpkrs_train_indx))
            #print(aSpkrs_cv_indx[0],aSpkrs_train_indx[0],iPnt)
            aCV[iCV][1] = np.r_[aCV[iCV][1],aSpkrs_cv_indx].astype(int)
            if sDataset_Name != 'UXTDD': #This if should be removed, added only for test OGI data
                aCV[iCV][0] = np.r_[aCV[iCV][0],aSpkrs_train_indx].astype(int)
            #print(iCV+1,aCV[iCV][1].shape, aCV[iCV][0].shape)
        iPnt += X.shape[0]
        #print(iPnt)
    X_all = X_all[:iPnt]
    y_all = y_all[:iPnt]
    #Get Statistics
    for i in range(len(aCV)):
        cv = aCV[i]
        print(str(i),';'.join(np.bincount(y_all[cv[0]]).astype(str)),';'.join(np.bincount(y_all[cv[1]]).astype(str)))

    return X_all, y_all, np.asarray(aSpkrs_all,dtype=str), aCV









#    #i/p --> Array of tuples each (list_of_waves,list_train_speakers,list_test_speakers,class)
    


