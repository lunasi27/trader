import datetime
import numpy as np
import pandas as pd
import tushare as ts
import pdb
#import pandas_datareader.data as web


class Stock():
    def __init__(self, data_source='yahoo'):
        self.data_source = data_source

    def collectData(self, stock_id, begin_date=None, end_date=None):
        if begin_date is None:
            begin_date = '2018-01-01'
        if end_date is None:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        #self.df = web.DataReader(stock, self.data_source, begin_date, end_date)
        self.df = ts.get_hist_data(stock_id, start=begin_date, end=end_date)
        #Change to ascending sorting
        self.df.sort_index(inplace=True)
        #Change index type into datetime
        self.df.index = pd.to_datetime(self.df.index)

    def calculateMA(self):
        #self.df['Ma20'] = self.df.close.rolling(window=20).mean()
        self.df['ma30'] = self.df.close.rolling(window=30).mean()
        self.df['ma60'] = self.df.close.rolling(window=60).mean()




if __name__ == '__main__':
    cvr = Stock()
    cvr.collectData('600797')
    print(cvr.df)
