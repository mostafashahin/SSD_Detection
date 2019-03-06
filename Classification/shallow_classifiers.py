from sklearn.svm import SVC
from joblib import dump, load
import numpy as np
import datetime as DT
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, make_scorer, balanced_accuracy_score
#svm params
estimators = {}
C = [100,10,1,0.1,0.01,0.001]
gamma = [100,10,1,0.1,0.01,0.001]
#kernels = ['linear','rbf','sigmoid','poly']
dParams_SVC_linear = {'SVM__kernel':['linear'],'SVM__C':C}
dParams_SVC_rbf_gamma = {'SVM__kernel':['rbf','sigmoid'],'SVM__C':C,'SVM__gamma':gamma}
estimators[SVC()] = ['SVM',dParams_SVC_linear,dParams_SVC_rbf_gamma]

Scaler = MinMaxScaler()

def GridSearchShallow(X, y, cv = 5, bSave_Model = False, prefix = ''):
    aTrainedModels = []
    for estimator in estimators:
        name, aParams = estimators[estimator][0],estimators[estimator][1:]
        pipline = Pipeline([('scaler',Scaler),(name,estimator)])
        scorer = make_scorer(balanced_accuracy_score)
        classifier = GridSearchCV(estimator = pipline, cv = cv, param_grid = aParams, verbose = 5, n_jobs = 1,scoring=scorer)
        classifier.fit(X,y)
        print(name,classifier.best_params_,classifier.best_score_)
        aTrainedModels.append(classifier)
        if bSave_Model:
            dump(classifier,name+'_'+str(DT.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+prefix+'.jbl')
    return aTrainedModels

#The estimator could be a pipeline with transformers and estimator
def Score_CV(estimator, X, y, cv = None, aSpeaker_List = [], bSpkrLevel = 'None', scorers = [('balanced_accuracy_score',balanced_accuracy_score)]):
    y_ref = np.zeros(0,dtype=int)
    y_predict = np.zeros(0,dtype=int)
    for part in cv:
        X_train, y_train = X[part[0]], y[part[0]]
        X_test, y_test = X[part[1]], y[part[1]]
        estimator.fit(X_train,y_train)
        y_p = estimator.predict(X_test)
        y_ref = np.r_[y_ref,y_test]
        y_predict = np.r_[y_predict,y_p]
    for scorer in scorers:
        print(scorer[0],str(scorer[1](y_ref,y_predict)))
    return y_ref, y_predict






