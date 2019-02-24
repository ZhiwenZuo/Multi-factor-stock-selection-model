#Data preparation
import pandas as pd
import numpy as np
import os 
os.chdir('E:/Brandeis/Brandeis/Second semester/Dissertation/Multi-factor stock selection mode/dataset')
#Firm selection
"""
x = companylist['Listdt'][0]
y = time.strptime(x,'%Y-%m-%d')
time.strftime('%Y-%m-%d', y)
"""
#select SH $ SZ A shares
def CompanyData():
    companylist = pd.read_table('Company information.txt', 
                            dtype={'Stkcd':str})
    condition = (companylist['Curtrd']=='CNY'
                )&(companylist['Ipocur']=='CNY'
                  )&(companylist['Parvcur']=='CNY'
                    )&((companylist['Markettype']==1
                      )|(companylist['Markettype']==4)) 
    companylist = companylist.loc[condition]
    variable = ['Stkcd','Stknme','Nnindcd','Nnindnme','Listdt','Sctcd']
    companylist = companylist[variable]
    return(companylist)
companylist = CompanyData()

#input data

def DataInput(company=companylist):
    #monthly stock return yield
    def MonthReturn():
        MonthReturn = pd.read_table('Stock return yield.txt', 
                            dtype={'Stkcd':str})
        condition = (MonthReturn['Trdmnt']>='2002-01')&(MonthReturn['Trdmnt']<='2017-12')
        MonthReturn = MonthReturn.loc[condition]
        variable = ['Stkcd','Trdmnt','Dturn','Mretnd']
        MonthReturn = MonthReturn[variable]
        #quarterly turnover rate
        def QDturn():
            QDturn = [np.NaN for i in range(len(MonthReturn))]
            for i in range(len(MonthReturn)-2):
                QDturn[i+2] = sum(MonthReturn['Dturn'].iloc[i:i+3])
            return(QDturn)
        MonthReturn['QDturn'] = QDturn()
        #quarterly stock return yield
        def QMretnd():
            QMretnd = [np.NaN for i in range(len(MonthReturn))]
            def multi(m):
                m = list(m)
                return((m[0]+1)*(m[1]+1)*(m[2]+1)-1)
            for i in range(len(MonthReturn)-2):
                QMretnd[i+2] = multi(MonthReturn['Mretnd'].iloc[i:i+3])
            return(QMretnd)
        MonthReturn['QMretnd'] = QMretnd()
        variable = ['Stkcd','Trdmnt','QDturn','QMretnd']
        MonthReturn = MonthReturn[variable].rename(columns={'Trdmnt':'Month'})    
        return(MonthReturn)
    MonthReturn = MonthReturn()
    
    #Index return
    def IndexReturn():
        IndexReturn = pd.read_table('Index return.txt', 
                            dtype={'Indexcd':str})
        condition = (IndexReturn['Month']>='2002-01')&(IndexReturn['Month']<='2017-12')
        IndexReturn = IndexReturn.loc[condition]
        variable = ['Indexcd','Month','Idxrtn']
        IndexReturn = IndexReturn[variable]
        # quarterly index return
        def QIdxrtn():
            QIdxrtn = ['' for i in range(len(IndexReturn))]
            def multi(m):
                m = list(m)
                return((m[0]+1)*(m[1]+1)*(m[2]+1)-1)
            for i in range(len(IndexReturn)-2):
                QIdxrtn[i+2] = multi(IndexReturn['Idxrtn'].iloc[i:i+3])
            return(QIdxrtn)
        IndexReturn['QIdxrtn'] = QIdxrtn()
        variable = ['Month','QIdxrtn']
        IndexReturn = IndexReturn[variable]
        return(IndexReturn)
    IndexReturn = IndexReturn()
    
    Data = pd.merge(MonthReturn,IndexReturn,on='Month')
    
    #current rate
    def FLCR():
        FLCR = pd.read_table('Current rate.txt', 
                            dtype={'Stkcd':str})
        condition = (FLCR['Accper']>='2002-01-01')&(FLCR['Accper']<='2017-12-31')
        FLCR = FLCR.loc[condition]
        def Month(date):
            return('-'.join(date.split('-')[0:2]))
        FLCR['Accper'] = list(map(Month,FLCR['Accper']))
        FLCR = FLCR.rename(columns={'Accper':'Month','F010101A':'CR'})
        return(FLCR)
    FLCR = FLCR()
    
    Data = pd.merge(Data,FLCR)
    
    #Price/Book Value
    def FLPB():
        FLPB = pd.read_table('PriceBook value.txt', 
                            dtype={'Stkcd':str})
        condition = (FLPB['Accper']>='2002-01-01')&(FLPB['Accper']<='2017-12-31')
        FLPB = FLPB.loc[condition]
        def Month(date):
            return('-'.join(date.split('-')[0:2]))
        FLPB['Accper'] = list(map(Month,FLPB['Accper']))
        FLPB = FLPB.rename(columns={'Accper':'Month','F091001A':'PB'})
        return(FLPB)
    FLPB = FLPB()
    
    Data = pd.merge(Data,FLPB)
    # Price-to-sales
    def FLPS():
        FLPS = pd.read_table('Pricetosales.txt', 
                    dtype={'Stkcd':str})
        condition = (FLPS['Accper']>='2002-01-01')&(FLPS['Accper']<='2017-12-31')
        FLPS = FLPS.loc[condition]
        def Month(date):
            return('-'.join(date.split('-')[0:2]))
        FLPS['Accper'] = list(map(Month,FLPS['Accper']))
        FLPS = FLPS.rename(columns={'Accper':'Month','F100201B':'PS'})
        return(FLPS)
    FLPS = FLPS()
    
    Data = pd.merge(Data,FLPS)
    # Profitability
    def FLPF():
        FLPF = pd.read_table('Profitability.txt', 
                            dtype={'Stkcd':str})
        condition = (FLPF['Accper']>='2002-01-01')&(FLPF['Accper']<='2017-12-31')
        FLPF = FLPF.loc[condition]
        def Month(date):
            return('-'.join(date.split('-')[0:2]))
        FLPF['Accper'] = list(map(Month,FLPF['Accper']))
        FLPF = FLPF.rename(columns={'Accper':'Month','F050201B':'ROA','F050501B':'ROE','F051501B':'NSR'})
        return(FLPF)
    FLPF = FLPF()
    
    Data = pd.merge(Data,FLPF)  
    
    return(Data)

Data = DataInput()
Data.dropna(inplace=True)
Data = Data.reset_index()
Data.drop(np.where(Data[['Stkcd','Month']].duplicated())[0],inplace=True)
Data.drop('index',1,inplace=True)

#
Data = Data.loc[Data['Month']>='2012-03']

#
timelist = Data['Month'].unique()

#estimation factor
def target(data=Data):
    #Value
    def NQMret():
        NQMret = [np.NaN for i in range(len(data))]
        for i in range(len(data)):
            try:
                time = data['Month'].iloc[i]
                time_ = timelist[np.where(timelist==time)[0]+1][0]
                k = data['Stkcd'].iloc[i]
                position = (data['Stkcd']==k)&(data['Month']==time_)
                NQMret[i] = data.loc[position].iloc[0,3]
            except: pass
        return(NQMret)
    data['NQMret'] = NQMret()
    
    #binary classfication 
    def NQMclass2():
        NQMclass2 = [np.NaN for i in range(len(data))]
        for i in range(len(data)-1):
            if data['NQMret'].iloc[i]>0:
                NQMclass2[i] = 1
            elif data['NQMret'].iloc[i]<0:
                NQMclass2[i] = 0
        return(NQMclass2)
    data['NQMclass2'] = NQMclass2()
    
    #5five level classfication
    def NQMclass5():
        NQMclass5 = [np.NaN for i in range(len(data))]
        for i in range(len(data)-1):
            if data['NQMret'].iloc[i]>0.05:
                NQMclass5[i] = 2
            elif data['NQMret'].iloc[i]>0.01: 
                NQMclass5[i] = 1
            elif data['NQMret'].iloc[i]>-0.01:
                NQMclass5[i] = 0
            elif data['NQMret'].iloc[i]>-0.05:
                NQMclass5[i] = -1
            elif data['NQMret'].iloc[i]<-0.05:
                NQMclass5[i] = -2
        return(NQMclass5)
    data['NQMclass5'] = NQMclass5()

    return(data)

Data = target()

#clean the data
Data.dropna(inplace=True)
Data = Data.reset_index()
Data.drop('index',1,inplace=True)

#save
companylist.to_csv('companylist.csv',index=False)
Data.to_csv('df.csv',index=False)