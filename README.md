# SSD_Detection
In this project I'm going to design a screening tool to detect the children with SSD from thier speech.
Algorithm:
1- I'll use eGeMAPs features as in https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf

2- I'll try a) inary SVM. 2) Anomaly Detection e.g. One-Class SVM.

3- Dataset: UltraSuite https://ultrasuite.github.io/

Feature Extraction:
- openSmile toolkit https://www.audeering.com/opensmile/

Dataset Description:
1- uxtd ---- > TD Children. uxssd -----> first SSD children group. upx -------> second SSD children group.

2- Tasks, https://ultrasuite.github.io/data/data/
   will use A, B, C, F

3- For SSD data, initially will use BaseLine sesssions (BL)

4- I'll use also the OGI dataset ages,code (k - 0,b), (1 - 1,c), (2 - 2,d), (3 - 3,e), (4 - 4,f), (5 - 5,g), (6 - 6,h), (7 - 7,i), (8 - 8,j), (9 - 9,k), (10 - a,l)


Experiments:

Expriement #1:

- GeMAPs features extracted from each segment
- Normalization using MinMax [0,1]
- Perform Segment Classification TD vs SSD
- Using UltraSuite uxtd, uxssd
- SVM Binary classsifier
- kernels = ['linear', 'rbf', 'sigmoid']
- gamma = [100,10,1,0.1,1e-2,1e-3,1e-4]
- C = [100,10,1,0.1,1e-2,1e-3,1e-4]
- dParams = {'kernel':kernels,'gamma':gamma,'C':C}

- Results:
 -- uxssd (5 train (2485), 3 test (1914)), uxtd (39 train (3344), 18 test (1425))
 -- ACC = 0.5443690637720489
 -- Param = {'C': 10, 'gamma': 1, 'kernel': 'rbf'}
 -- uxssd (6 train, 2 test)
 -- ACC: 0.5390835579514824
 -- best_params_ {'C': 100, 'gamma': 1, 'kernel': 'rbf'}

Expriement #2:

- GeMAPs features extracted from each segment
- Normalization using MinMax [0,1]
- Perform Segment Classification TD vs SSD
- Using UltraSuite uxtd, upx
- SVM Binary classsifier
- kernels = ['linear', 'rbf', 'sigmoid']
- gamma = [100,10,1,0.1,1e-2,1e-3,1e-4]
- C = [100,10,1,0.1,1e-2,1e-3,1e-4]
- dParams = {'kernel':kernels,'gamma':gamma,'C':C}

- Results:
 -- upx (14 train (6196), 6 test (2521)), uxtd (40 train (3344), 18 test (1425))
 -- ACC = 0.8613786112519006
 -- Param = {'C': 10, 'gamma': 1, 'kernel': 'rbf'}

Expriement #3:

- GeMAPs features extracted from each segment
- Normalization using MinMax [0,1]
- Perform Segment Classification TD vs SSD
- Using all the speakers UXTD, UXSSD, UPX (28 SSD, 58 TD)
- 4 fold CV, each has (Training (21 SSD, 51 TD), Validation (7 SSD, 7 TD))
- The children from SSD and TD age and gender matching when possible
- The normalization fit on the training portion only for each CV
- kernels = ['linear', 'rbf', 'sigmoid']
- gamma = [100,10,1,0.1,1e-2,1e-3,1e-4]
- C = [100,10,1,0.1,1e-2,1e-3,1e-4]

- Results:
 -- {'SVM__C': 0.1, 'SVM__gamma': 10, 'SVM__kernel': 'rbf'}
 -- average 0.8501616031027796

XXXXXXXXXXXXXXXXXXXXXXXXXXPrevious results not accurateXXXXXXXXXXXXXX

Expriement #3+:

- GeMAPs features extracted from each segment
- Normalization using MinMax [0,1]
- Perform Segment Classification TD vs SSD
- Using all the speakers UXTD, UXSSD, UPX (28 SSD, 58 TD)
- Two BL sessions from UXSSD and UPX, A, B, C, F
- 4 250000.0
- UXTD 1 0 0
- UXSSD 1 8 4399
- UPX 1 20 8708
- 0 4287;9758 482;3349
- 1 3995;9895 774;3212
- 2 4365;10298 404;2809
- 3 4066;9370 703;3737
- 4 fold CV, each has (Training (21 SSD, 51 TD), Validation (7 SSD, 7 TD))
- The children from SSD and TD age and gender matching when possible
- The normalization fit on the training portion only for each CV
- ---- the metrics is balanced_score because the number of segments of the SSD children is much greater than the typically development. 
- kernels = ['linear', 'rbf', 'sigmoid']
- gamma = [100,10,1,0.1,1e-2,1e-3,1e-4]
- C = [100,10,1,0.1,1e-2,1e-3,1e-4]

- Results
- -- SVM {'SVM__C': 100, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} 0.7303084431415353

Experiment 4:

- Same setup of 3+
- Features eGeMAPs

- Results
- -- SVM {'SVM__C': 10, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} 0.759606545167094 MaxMin Normalization
- -- SVM {'SVM__C': 10, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.7570786436031008 z normalization


Experiment 5:
- Same setup of 3+
- Use only one BL session and exclude "F: conversation files" from the SSD data to reduce the number of segments from SSD to balance the model

- Results
- --{'SVM__C': 10, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} 0.7593882264312595 (Segment level)
0.875 (Speaker level)
01F_UPX [ 11 213] 1 1 1
02F_UPX [ 57 232] 1 1 1
03F_UPX [ 2 89] 1 1 1
03F_UXSSD [342 150] 0 1 1
06M_UXSSD [ 61 313] 1 1 1
07F_UXSSD [ 13 188] 1 1 1
18F_UPX [ 13 166] 1 1 1
18F_UXTD [54  9] 0 0 0
24F_UXTD [128  19] 0 0 0
26F_UXTD [96 25] 0 0 0
33F_UXTD [34 14] 0 0 0
36M_UXTD [25  8] 0 0 0
41F_UXTD [26 14] 0 0 0
48F_UXTD [22  8] 0 0 0
01M_UXSSD [131  40] 0 1 1
05M_UPX [ 12 184] 1 1 1
05M_UXSSD [ 78 328] 1 1 1
05M_UXTD [117  16] 0 0 0
06M_UPX [ 12 205] 1 1 1
08M_UXTD [107  25] 0 0 0
11M_UPX [ 44 169] 1 1 1
11M_UXTD [103  30] 0 0 0
12M_UPX [ 73 352] 1 1 1
12M_UXTD [88 52] 0 0 0
15M_UPX [241 110] 0 1 1
17M_UXTD [107  46] 0 0 0
37M_UXTD [30 12] 0 0 0
38M_UXTD [27 14] 0 0 0
04M_UPX [217  79] 0 1 1
07M_UPX [ 83 164] 1 1 1
08M_UXSSD [143  81] 0 1 1
09M_UPX [ 13 184] 1 1 1
13M_UPX [ 20 295] 1 1 1
14M_UPX [ 10 107] 1 1 1
15M_UXTD [42  8] 0 0 0
16M_UPX [ 51 272] 1 1 1
22M_UXTD [125  15] 0 0 0
35M_UXTD [25  7] 0 0 0
42M_UXTD [25 11] 0 0 0
51M_UXTD [35  8] 0 0 0
55M_UXTD [23  3] 0 0 0
56M_UXTD [57 20] 0 0 0
02M_UXSSD [199  81] 0 1 1
04M_UXSSD [ 81 629] 1 1 1
04M_UXTD [155  20] 0 0 0
08M_UPX [ 26 173] 1 1 1
10M_UPX [ 36 256] 1 1 1
14M_UXTD [127  36] 0 0 0
17M_UPX [ 37 139] 1 1 1
19M_UPX [198 111] 0 1 1
19M_UXTD [98 41] 0 0 0
20M_UPX [126 145] 1 1 1
25M_UXTD [86 51] 0 0 0
34M_UXTD [20 11] 0 0 0
40M_UXTD [21  8] 0 0 0
45M_UXTD [22  7] 0 0 0


Experiment 6:
- Same setup of 4
- Use only one BL session and exclude "F: conversation files" from the SSD data to reduce the number of segments from SSD to balance the model
4 250000.0
UXTD 1 0 0
UXSSD 1 8 2858
UPX 1 20 4927
0 4287;5935 482;1850
1 3995;5806 774;1979
2 4365;6066 404;1719
3 4066;5548 703;2237


- Results:
- -- SVM {'SVM__C': 10, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} Segment level (0.7882262068336758) Normalization (MaxMin) speaker level (0.8571428571428572)
- -- SVM {'SVM__C': 10, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.7851423804412466 Normalization (z normalize)
01F_UPX [ 10 214] 1 1 1
02F_UPX [ 43 246] 1 1 1
03F_UPX [ 4 87] 1 1 1
03F_UXSSD [327 165] 0 1 1
06M_UXSSD [ 72 302] 1 1 1
07F_UXSSD [ 13 188] 1 1 1
18F_UPX [ 16 163] 1 1 1
18F_UXTD [57  6] 0 0 0
24F_UXTD [132  15] 0 0 0
26F_UXTD [99 22] 0 0 0
33F_UXTD [34 14] 0 0 0
36M_UXTD [25  8] 0 0 0
41F_UXTD [27 13] 0 0 0
48F_UXTD [25  5] 0 0 0
01M_UXSSD [129  42] 0 1 1
05M_UPX [ 12 184] 1 1 1
05M_UXSSD [ 90 316] 1 1 1
05M_UXTD [122  11] 0 0 0
06M_UPX [ 11 206] 1 1 1
08M_UXTD [110  22] 0 0 0
11M_UPX [ 33 180] 1 1 1
11M_UXTD [106  27] 0 0 0
12M_UPX [ 89 336] 1 1 1
12M_UXTD [89 51] 0 0 0
15M_UPX [264  87] 0 1 1
17M_UXTD [100  53] 0 0 0
37M_UXTD [29 13] 0 0 0
38M_UXTD [23 18] 0 0 0
04M_UPX [209  87] 0 1 1
07M_UPX [ 88 159] 1 1 1
08M_UXSSD [141  83] 0 1 1
09M_UPX [ 18 179] 1 1 1
13M_UPX [ 19 296] 1 1 1
14M_UPX [  8 109] 1 1 1
15M_UXTD [44  6] 0 0 0
16M_UPX [ 42 281] 1 1 1
22M_UXTD [128  12] 0 0 0
35M_UXTD [27  5] 0 0 0
42M_UXTD [27  9] 0 0 0
51M_UXTD [37  6] 0 0 0
55M_UXTD [21  5] 0 0 0
56M_UXTD [58 19] 0 0 0
02M_UXSSD [193  87] 0 1 1
04M_UXSSD [ 92 618] 1 1 1
04M_UXTD [161  14] 0 0 0
08M_UPX [ 23 176] 1 1 1
10M_UPX [ 29 263] 1 1 1
14M_UXTD [131  32] 0 0 0
17M_UPX [ 39 137] 1 1 1
19M_UPX [230  79] 0 1 1
19M_UXTD [102  37] 0 0 0
20M_UPX [149 122] 0 1 1
25M_UXTD [80 57] 0 0 0
34M_UXTD [22  9] 0 0 0
40M_UXTD [18 11] 0 0 0
45M_UXTD [19 10] 0 0 0



NOTE: MaxMin normalization converge faster than the std and almost same performance, so only MaxMin is used in upcoming exps.

Exp. 7:
- Apply feature selection RFECV on GeMAPs (62 features)
- Ranking using linear SVM with C=10 (best linear SVM on segment level)
- 55 features selected
F0semitoneFrom27.5Hz_sma3nz_amean
F0semitoneFrom27.5Hz_sma3nz_percentile20.0
F0semitoneFrom27.5Hz_sma3nz_percentile50.0
F0semitoneFrom27.5Hz_sma3nz_percentile80.0
F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2
F0semitoneFrom27.5Hz_sma3nz_stddevRisingSlope
F0semitoneFrom27.5Hz_sma3nz_stddevFallingSlope
loudness_sma3_amean
loudness_sma3_stddevNorm
loudness_sma3_percentile20.0
loudness_sma3_percentile50.0
loudness_sma3_percentile80.0
loudness_sma3_pctlrange0-2
loudness_sma3_meanRisingSlope
loudness_sma3_meanFallingSlope
loudness_sma3_stddevFallingSlope
jitterLocal_sma3nz_amean
jitterLocal_sma3nz_stddevNorm
shimmerLocaldB_sma3nz_amean
shimmerLocaldB_sma3nz_stddevNorm
HNRdBACF_sma3nz_amean
HNRdBACF_sma3nz_stddevNorm
logRelF0-H1-A3_sma3nz_amean
logRelF0-H1-A3_sma3nz_stddevNorm
F1frequency_sma3nz_amean
F1frequency_sma3nz_stddevNorm
F1bandwidth_sma3nz_amean
F1bandwidth_sma3nz_stddevNorm
F1amplitudeLogRelF0_sma3nz_stddevNorm
F2frequency_sma3nz_amean
F2frequency_sma3nz_stddevNorm
F2amplitudeLogRelF0_sma3nz_stddevNorm
F3frequency_sma3nz_amean
F3frequency_sma3nz_stddevNorm
F3amplitudeLogRelF0_sma3nz_amean
F3amplitudeLogRelF0_sma3nz_stddevNorm
alphaRatioV_sma3nz_stddevNorm
hammarbergIndexV_sma3nz_amean
hammarbergIndexV_sma3nz_stddevNorm
slopeV0-500_sma3nz_amean
slopeV500-1500_sma3nz_amean
slopeV500-1500_sma3nz_stddevNorm
alphaRatioUV_sma3nz_amean
hammarbergIndexUV_sma3nz_amean
slopeUV0-500_sma3nz_amean
slopeUV500-1500_sma3nz_amean
loudnessPeaksPerSec
VoicedSegmentsPerSec
MeanVoicedSegmentLengthSec
StddevVoicedSegmentLengthSec
MeanUnvoicedSegmentLength
StddevUnvoicedSegmentLength

- Results:
- --{'SVM__C': 10, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} Segment level (0.7559353565352006) Speaker level (0.875)
01F_UPX [ 10 214] 1 1 1
02F_UPX [ 57 232] 1 1 1
03F_UPX [ 1 90] 1 1 1
03F_UXSSD [341 151] 0 1 1
06M_UXSSD [ 65 309] 1 1 1
07F_UXSSD [ 11 190] 1 1 1
18F_UPX [ 12 167] 1 1 1
18F_UXTD [56  7] 0 0 0
24F_UXTD [127  20] 0 0 0
26F_UXTD [99 22] 0 0 0
33F_UXTD [33 15] 0 0 0
36M_UXTD [25  8] 0 0 0
41F_UXTD [26 14] 0 0 0
48F_UXTD [20 10] 0 0 0
01M_UXSSD [127  44] 0 1 1
05M_UPX [ 11 185] 1 1 1
05M_UXSSD [ 84 322] 1 1 1
05M_UXTD [117  16] 0 0 0
06M_UPX [ 10 207] 1 1 1
08M_UXTD [110  22] 0 0 0
11M_UPX [ 45 168] 1 1 1
11M_UXTD [103  30] 0 0 0
12M_UPX [ 73 352] 1 1 1
12M_UXTD [85 55] 0 0 0
15M_UPX [237 114] 0 1 1
17M_UXTD [108  45] 0 0 0
37M_UXTD [28 14] 0 0 0
38M_UXTD [30 11] 0 0 0
04M_UPX [215  81] 0 1 1
07M_UPX [ 86 161] 1 1 1
08M_UXSSD [141  83] 0 1 1
09M_UPX [ 15 182] 1 1 1
13M_UPX [ 17 298] 1 1 1
14M_UPX [  9 108] 1 1 1
15M_UXTD [44  6] 0 0 0
16M_UPX [ 53 270] 1 1 1
22M_UXTD [124  16] 0 0 0
35M_UXTD [26  6] 0 0 0
42M_UXTD [26 10] 0 0 0
51M_UXTD [35  8] 0 0 0
55M_UXTD [24  2] 0 0 0
56M_UXTD [56 21] 0 0 0
02M_UXSSD [200  80] 0 1 1
04M_UXSSD [ 82 628] 1 1 1
04M_UXTD [155  20] 0 0 0
08M_UPX [ 25 174] 1 1 1
10M_UPX [ 36 256] 1 1 1
14M_UXTD [132  31] 0 0 0
17M_UPX [ 36 140] 1 1 1
19M_UPX [196 113] 0 1 1
19M_UXTD [94 45] 0 0 0
20M_UPX [130 141] 1 1 1
25M_UXTD [86 51] 0 0 0
34M_UXTD [20 11] 0 0 0
40M_UXTD [21  8] 0 0 0
45M_UXTD [20  9] 0 0 0

Exp. 8:
- Apply feature selection RFECV on eGeMAPs (88 features)
- Ranking using linear SVM with C=10 (best linear SVM on segment level)
- Also 55 features selected:
F0semitoneFrom27.5Hz_sma3nz_amean
F0semitoneFrom27.5Hz_sma3nz_percentile50.0
F0semitoneFrom27.5Hz_sma3nz_percentile80.0
F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2
loudness_sma3_amean
loudness_sma3_stddevNorm
loudness_sma3_percentile20.0
loudness_sma3_percentile50.0
loudness_sma3_percentile80.0
loudness_sma3_stddevRisingSlope
loudness_sma3_meanFallingSlope
loudness_sma3_stddevFallingSlope
spectralFlux_sma3_stddevNorm
mfcc1_sma3_amean
mfcc2_sma3_amean
mfcc2_sma3_stddevNorm
mfcc3_sma3_amean
mfcc4_sma3_amean
jitterLocal_sma3nz_amean
jitterLocal_sma3nz_stddevNorm
shimmerLocaldB_sma3nz_amean
shimmerLocaldB_sma3nz_stddevNorm
HNRdBACF_sma3nz_amean
HNRdBACF_sma3nz_stddevNorm
logRelF0-H1-A3_sma3nz_stddevNorm
F1frequency_sma3nz_amean
F1bandwidth_sma3nz_amean
F2bandwidth_sma3nz_amean
F2amplitudeLogRelF0_sma3nz_amean
F2amplitudeLogRelF0_sma3nz_stddevNorm
F3frequency_sma3nz_amean
F3amplitudeLogRelF0_sma3nz_stddevNorm
alphaRatioV_sma3nz_amean
alphaRatioV_sma3nz_stddevNorm
hammarbergIndexV_sma3nz_amean
slopeV0-500_sma3nz_amean
slopeV500-1500_sma3nz_amean
spectralFluxV_sma3nz_amean
mfcc1V_sma3nz_amean
mfcc1V_sma3nz_stddevNorm
mfcc2V_sma3nz_amean
mfcc2V_sma3nz_stddevNorm
mfcc3V_sma3nz_amean
mfcc3V_sma3nz_stddevNorm
mfcc4V_sma3nz_amean
mfcc4V_sma3nz_stddevNorm
alphaRatioUV_sma3nz_amean
hammarbergIndexUV_sma3nz_amean
slopeUV0-500_sma3nz_amean
slopeUV500-1500_sma3nz_amean
spectralFluxUV_sma3nz_amean
loudnessPeaksPerSec
VoicedSegmentsPerSec
MeanUnvoicedSegmentLength
equivalentSoundLevel_dBp

- Results:
- --{'SVM__C': 10, 'SVM__gamma': 1, 'SVM__kernel': 'rbf'} Segment level (0.7872807662134181), Speaker level (0.875)


Exp.9 :
- Enabling the balanced feature in SVM imp. of slearn.
- Using BL1 and BL2 from disorder data
- GeMaps features (62)
- Same CV setting


- Results:
- -- {'SVM__C': 100, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.7592546676585075 (Segment level) 0.8571428571428572

Exp. 10 : 
- Enabling the balanced feature in SVM imp. of slearn.
- Using BL1 and BL2 from disorder data
- eGeMaps features (88)
- Same CV setting


- Results:
- {'SVM__C': 10, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.777557758657335 (segment lev)
0.8571428571428571 

Exp. 11 : Exclude short segments < 0.5 sec
- Enabling the balanced feature in SVM imp. of slearn.
- Using BL1 and BL2 from disorder data
- GeMaps features (62)
- Same CV setting

- Results:
- -- SVM {'SVM__C': 100, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.7789681889052708 (SegLevel) 0.8392857142857143 (SpkLevel)

Exp. 12 : Exclude short segments < 0.5 sec
- Enabling the balanced feature in SVM imp. of slearn.
- Using BL1 and BL2 from disorder data
- eGeMaps features (88)
- Same CV setting


- Results:
- -- SVM {'SVM__C': 10, 'SVM__gamma': 0.01, 'SVM__kernel': 'rbf'} 0.7993435496111929 (SegLevel) 0.8214285714285714 (SpkLevel)

TO DO************************************************************
1. report results on speaker level (Done)
2. feature selection (Done RFE)
3. eGeMAPs features (Done)
4. ComParE features
5. Anomaly detection, OCSVM, LSTM
6. In segment performance use F1 score and show confusion matrix (I used UAR and confusion matrix)
7. In Anomaly detection use more healthy data, OREGON
8. Use the ASD data for reporting result of Anomaly detection
9. Use of our CAS dataset
10. Try data augmentation to increase the number of samples in the TD, maybe dublication of randomly selected samples. 
