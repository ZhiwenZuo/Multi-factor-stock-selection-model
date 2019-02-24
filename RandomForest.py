
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np


df = pd.read_csv('df.csv', 
                 dtype={'Stkcd':str})
companylist = pd.read_csv('companylist.csv', 
                 dtype={'Stkcd':str})

#Data preparation
def is_train(df=df):
    number_train = round(len(df)*0.1)
    is_train = np.append(np.ones(number_train),np.zeros(len(df)-number_train))
    np.random.shuffle(is_train)
    return(is_train)
is_train = is_train()


train, test = df[is_train==True], df[is_train==False]

features = df.columns[2:11]



#binary classfication
def class2(ntree=20, train=train,test=test):
    clf = RandomForestClassifier(n_jobs=2, oob_score=True, n_estimators=ntree)
    clf.fit(train[features], train['NQMclass2'])
    return(clf)
clf2 = class2(20)
preds = clf2.predict(test[features])
print(pd.crosstab(test['NQMclass2'], preds, rownames=['actual'], colnames=['preds']))
print(clf2.oob_score_)
pd.DataFrame({'features':features,'importance':clf2.feature_importances_}).to_csv('features.csv')  
print(clf2.predict(test[features])[:10],clf2.predict_proba(test[features])[:10])

#oob error
k = []
numb = []
for i in range(30):
    numb.append(i+1)
    clf2 = class2(i+1)
    k.append(clf2.oob_score_)
ntree = pd.DataFrame({'ntree':numb,'oob':k})
ntree.to_csv('ntree.csv')

#To find the optimal numble of trees based on greedy algorithm
from sklearn.model_selection import GridSearchCV 
param_test1= {'n_estimators':[i for i in range(10,50,5)]}  
gsearch1= GridSearchCV(estimator = RandomForestClassifier(),  
                       param_grid =param_test1, scoring='roc_auc',cv=5)  
gsearch1.fit(train[features],train['NQMclass2'])  
gsearch1.cv_results_, gsearch1.best_score_  
print(gsearch1.best_params_)
# ntrees = 25

param_test2= {'max_depth':[i for i in range(1,6,1)], 'min_samples_split':[i for i in range(7,35,4)]}  
gsearch2= GridSearchCV(estimator = RandomForestClassifier(n_estimators= 25),  
   param_grid = param_test2,scoring='roc_auc',iid=False, cv=5)  
gsearch2.fit(train[features],train['NQMclass2'])   
gsearch2.cv_results_, gsearch2.best_params_, gsearch2.best_score_ 
print(gsearch2.best_params_)
#{'min_samples_split': 15}

#five factor classfication
def class5(train=train,test=test):
    clf = RandomForestClassifier(n_jobs=2, oob_score=True)
    clf.fit(train[features], train['NQMclass5'])
    return(clf)
clf5 = class5()
preds = clf5.predict(test[features])
print(pd.crosstab(test['NQMclass5'], preds, rownames=['actual'], colnames=['preds']))
print(clf5.oob_score_)
print(clf5.feature_importances_)
print(clf5.predict(test[features])[:10],clf5.predict_proba(test[features])[:10])

def regress(train=train,test=test):
    clf = RandomForestRegressor(n_jobs=2, oob_score=True)
    clf.fit(train[features], train['NQMret'])
    return(clf)
clfr = regress()
preds = clfr.predict(test[features])

print(pd.crosstab(test['NQMret'], preds, rownames=['actual'], colnames=['preds']))
