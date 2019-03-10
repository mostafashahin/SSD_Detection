from sklearn.svm import SVC
from joblib import dump, load
import numpy as np
import datetime as DT
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, make_scorer, balanced_accuracy_score
from sklearn.feature_selection import RFECV
#svm params
estimators = {}
C = [100,10,1,0.1,0.01,0.001]
gamma = [100,10,1,0.1,0.01,0.001]
#kernels = ['linear','rbf','sigmoid','poly']
dParams_SVC_linear = {'SVM__kernel':['linear'],'SVM__C':C}
dParams_SVC_rbf_gamma = {'SVM__kernel':['rbf','sigmoid'],'SVM__C':C,'SVM__gamma':gamma}
estimators[SVC()] = ['SVM',dParams_SVC_linear,dParams_SVC_rbf_gamma]

scaler = MinMaxScaler()
#Scaler = StandardScaler()

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






