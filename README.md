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


