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

