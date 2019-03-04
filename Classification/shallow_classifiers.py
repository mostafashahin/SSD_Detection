from sklearn.svm import SVC
from joblib import dump, load
import datetime as DT
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

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
        classifier = GridSearchCV(estimator = pipline, cv = cv, param_grid = aParams, verbose = 5, n_jobs = 1)
        classifier.fit(X,y)
        print(name,classifier.best_params_,classifier.best_score_)
        aTrainedModels.append(classifier)
        if bSave_Model:
            dump(classifier,name+'_'+str(DT.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+prefix+'.jbl')
    return aTrainedModels





