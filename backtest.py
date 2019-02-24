#backtest
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

df = pd.read_csv('df.csv', 
                 dtype={'Stkcd':str})
companylist = pd.read_csv('companylist.csv', 
                 dtype={'Stkcd':str})
trainlist = df['Stkcd'].unique()  
testlist = companylist['Stkcd'].loc[companylist['Stkcd'].isin(trainlist)] 

#exclude PT&ST Company
def subst(clist = companylist):
    cname = clist['Stknme']
    STPT = []
    for i in cname:
        STPT.append(('PT' not in i) and ('ST' not in i))
    return(clist.loc[STPT])
companylist = subst()        
    
class backtest:
    
    def __init__(self, 
        df=df, companylist=companylist):
        self.trainlist = trainlist
        self.testlist = testlist
        self.df = df
        self.companylist = companylist
        self.timelist = df['Month'].unique()
        
    #exclude the companies which are not on the companylist
    def cluster_list(self):
        self.df = df.loc[df['Stkcd'].isin(self.companylist['Stkcd'])]
        return(self.df)
    
    #return train dataset and test dataset   
    def train_test(self, month):
        monthsub8 = self.timelist[np.where(self.timelist==month)[0]-8][0]
        train = self.df.loc[(self.df['Month']<month)&(self.df['Month']>=monthsub8)]
        test = self.df.loc[(self.df['Month']==month)&(self.df['Stkcd'].isin(self.testlist))]
        return(train,test)
    

    #return the ranking of the companies 
    def companyrank(self, month, numberofcom):    
        
        train,test = backtest.train_test(self, month)
        
        features = self.df.columns[2:11]
        def regress(train=train):
            clf = RandomForestRegressor(n_jobs=2, n_estimators=25,min_samples_split=15)
            clf.fit(train[features], train['NQMret'])
            return(clf)
        
        clfr = regress()
        k = test[['Stkcd','Month','NQMret','QIdxrtn']].copy()
        k['preds'] = clfr.predict(test[features])
        k = k.sort_values(by=['preds'],ascending=False).iloc[:numberofcom]
        return(k)
    
    #return the yield of the portfolio
    def profit(self, month, numberofcom):
        
        test = backtest.companyrank(self, month, numberofcom)
        
        ret = np.average(test.loc[:,'NQMret'])
        ret_forecast = np.average(test.loc[:,'preds'])
        return(ret,ret_forecast)
    
    #market index return 
    def marketprofit(self, month): 
        month = self.timelist[np.where(self.timelist==month)[0]][0] ##!
        test =  self.df.loc[(self.df['Month']==month)] 
        market = test['QIdxrtn'].iloc[0]
        return(market)
    
    #return the yield, estimated yield and market yield for each period 
    def backtestor(self, period, numberofcom):
        market = []
        ret = []
        ret_forecast = []
        date = []
        timeline =  self.timelist[int(np.where(self.timelist==period[0])[0]):int(np.where(
                        self.timelist==period[1])[0]+1)]
        for month in timeline:
            r,r_f = backtest.profit(self, month, numberofcom)
            m = backtest.marketprofit(self, month)
            ret.append(r)
            ret_forecast.append(r_f)
            market.append(m)
            date.append(month)
            
        def cummulti(ret):
            cumret = []
            c = 1
            for i in ret:
                c = c*(i+1)
                cumret.append(c)
            return(cumret)
        cumret = cummulti(ret)
        cummarket = cummulti(market)    
                
        testresult = pd.DataFrame({'date':date,
                                   'ret':ret,
                                   'marketindex':market,
                                   'cumret':cumret,
                                   'cummarketret':cummarket},
                        columns=['date','ret','marketindex','cumret','cummarketret'])
        return(testresult)
        
    
bk = backtest()



result1 = bk.companyrank('2014-03',20)
profit = np.average(result1['NQMret'])
result1 = result1.merge(companylist[['Stkcd','Stknme','Nnindnme','Sctcd']])
result1.to_csv('result1.csv')

#回测
result10 = bk.backtestor(['2014-03','2017-06'],10)  # the portfolio we choose
result10.to_csv('result11.csv')
result20 = bk.backtestor(['2014-03','2017-06'],20)
result20.to_csv('result20.csv')
result30 = bk.backtestor(['2014-03','2017-06'],30)
result30.to_csv('result30.csv')
result50 = bk.backtestor(['2014-03','2017-06'],50)
result50.to_csv('result50.csv')
