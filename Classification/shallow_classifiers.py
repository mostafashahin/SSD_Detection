import numpy as np
import datetime as DT
import copy
from sklearn.svm import SVC, OneClassSVM
from joblib import dump, load
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, make_scorer, balanced_accuracy_score
from sklearn.feature_selection import RFECV
#svm params
estimators = {}
anomaly_detectors = {}
C = [100,10,1,0.1,0.01,0.001]
gamma = [100,10,1,0.1,0.01,0.001]
#kernels = ['linear','rbf','sigmoid','poly']
dParams_SVC_linear = {'SVM__kernel':['linear'],'SVM__C':C}
dParams_SVC_rbf_gamma = {'SVM__kernel':['rbf','sigmoid'],'SVM__C':C,'SVM__gamma':gamma}
estimators[SVC(class_weight='balanced')] = ['SVM',dParams_SVC_linear,dParams_SVC_rbf_gamma]

#oneclass SVM params
nu = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1]
dParams_OCSVM_linear = {'OCSVM__kernel':['linear'],'OCSVM__nu':nu}
dParams_OCSVM_rbf_gamma = {'OCSVM__kernel':['rbf','sigmoid'],'OCSVM__nu':nu,'OCSVM__gamma':gamma}
anomaly_detectors[OneClassSVM()] = ['OCSVM', dParams_OCSVM_linear, dParams_OCSVM_rbf_gamma]

scaler = MinMaxScaler(feature_range=(-3, 3))
#scaler = StandardScaler()

scorer = make_scorer(balanced_accuracy_score)

class PipelineRFE(Pipeline):
    def fit(self, X, y=None, **fit_params):
        super(PipelineRFE, self).fit(X, y, **fit_params)
        self.coef_ = self.steps[-1][-1].coef_
        return self
    
def GridSearchShallow(X, y, cv = 5, bSave_Model = False, prefix = '', verbose = 0, n_jobs = None):
    aTrainedModels = []
    for estimator in estimators:
        name, aParams = estimators[estimator][0],estimators[estimator][1:]
        pipline = Pipeline([('scaler',scaler),(name,estimator)])
        classifier = GridSearchCV(estimator = pipline, cv = cv, param_grid = aParams, verbose = verbose, n_jobs = n_jobs, scoring = scorer)
        classifier.fit(X,y)
        print(name, classifier.best_params_, classifier.best_score_)
        aTrainedModels.append(classifier)
        if bSave_Model:
            dump(classifier,name+'_'+str(DT.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+prefix+'.jbl')
    return aTrainedModels

def GridSearchAnomaly(X, y, cv=5, iMain_class = 0, bSave_Model = False, prefix = '', verbose = 0, n_jobs = None):
    aTrainedModels = []
    y_anomaly = copy.deepcopy(y)
    aMain_class_Mask = (y_anomaly == iMain_class)
    aAnomaly_Mask = np.invert(aMain_class_Mask)
    y_anomaly[aMain_class_Mask] = 1
    y_anomaly[aAnomaly_Mask] = -1
    if hasattr(cv,'__iter__'):
        cv_anomaly = copy.deepcopy(cv)
        for part in cv_anomaly:
            part[0] = np.intersect1d(part[0],np.where(y_anomaly==1)[0])

    print(y.min(),y.max(),y_anomaly.min(),y_anomaly.max())
    for part in cv_anomaly:
        print(part[0].shape,y_anomaly[part[0]].max(),y_anomaly[part[0]].min())#cv_anomaly[1][0].shape,cv_anomaly[2][0].shape,cv_anomaly[3][0].shape,cv_anomaly[4][0].shape,y_ano)
    for detector in anomaly_detectors:
        name, aParams = anomaly_detectors[detector][0], anomaly_detectors[detector][1:]
        pipline = Pipeline([('scaler',scaler),(name,detector)])
        classifier = GridSearchCV(estimator = pipline, cv = cv_anomaly, param_grid = aParams, verbose = verbose, n_jobs = n_jobs, scoring = scorer)
        classifier.fit(X,y_anomaly)
        print(name, classifier.best_params_, classifier.best_score_)
        aTrainedModels.append(classifier)
        if bSave_Model:
            dump(classifier,name+'_'+str(DT.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+prefix+'.jbl')
    return aTrainedModels

#The estimator could be a pipeline with transformers and estimator
def Score_CV(estimator, X, y, cv = 5, aSpeaker_List = [], SpkrLevel = 'None', scorers = [('balanced_accuracy_score',balanced_accuracy_score)],verbose=0):
    iDim = X.shape[1]
    y_ref = np.zeros(0,dtype=int)
    y_predict = np.zeros(0,dtype=int)
    #if SpkrLevel != 'None':
    y_ref_spk = np.zeros(0,dtype=int)
    y_predict_spk = np.zeros(0,dtype=int)
    for part in cv:
        X_train, y_train = X[part[0]], y[part[0]]
        X_test, y_test = X[part[1]], y[part[1]]
        estimator.fit(X_train,y_train)
        y_p = estimator.predict(X_test)
        y_ref = np.r_[y_ref,y_test]
        y_predict = np.r_[y_predict,y_p]
        spkrs_test = aSpeaker_List[part[1]]
        if SpkrLevel == 'average':
            X_test_spk = np.zeros((0,iDim),dtype=float)
            y_test_spk = np.zeros(0,dtype=int)
            for spkr in np.unique(spkrs_test):
                spkrs_ind = np.where(spkrs_test == spkr)
                X_tmp = X_test[spkrs_ind].mean(axis=0).reshape(1,iDim)
                #print(X_tmp.shape,X_test_spk.shape)
                X_test_spk = np.r_[X_test_spk,X_tmp]
                y_test_spk = np.r_[y_test_spk,y_test[spkrs_ind].max()]
            y_p_spk = estimator.predict(X_test_spk)
            y_ref_spk = np.r_[y_ref_spk,y_test_spk]
            y_predict_spk = np.r_[y_predict_spk,y_p_spk]
        elif SpkrLevel == 'major':
            for spkr in np.unique(spkrs_test):
                spkrs_ind = np.where(spkrs_test == spkr)
                y_p_spk = np.bincount(y_predict[spkrs_ind]).argmax()
                y_ref_spk = np.r_[y_ref_spk,y_test[spkrs_ind].max()]
                y_predict_spk = np.r_[y_predict_spk,y_p_spk]
                print(spkr,np.bincount(y_predict[spkrs_ind]),y_p_spk,y_test[spkrs_ind].max(),y_test[spkrs_ind].min())
                #print(y_ref_spk.shape,y_predict_spk.shape)

    for scorer in scorers:
        print(scorer[0],str(scorer[1](y_ref,y_predict)))
    if SpkrLevel != 'None':
        for scorer in scorers:
            print(scorer[0],str(scorer[1](y_ref_spk,y_predict_spk)))
    return y_ref, y_predict, y_ref_spk, y_predict_spk


def Feature_Selection(estimator,X,y,cv=5,verbose=0,n_jobs=None):
    pipline = PipelineRFE([('scaler',scaler),('clf',estimator)])
    selector = RFECV(pipline, cv=cv, verbose=verbose, scoring=scorer, n_jobs=n_jobs)
    selector.fit(X,y)
    return selector






