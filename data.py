import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web


class Stock():
    def __init__(self, data_source='yahoo'):
        self.data_source = data_source

    def collectData(self, stock_name, begin_date=None, end_date=None):
        if stock_name[0] == '6':
            stock = '%s.SS' % stock_name
        else:
            stock = '%s.SZ' % stock_name
        if begin_date is None:
            begin_date = datetime.datetime(2018,1,1)
        if end_date is None:
            end_date = datetime.datetime.now()
        self.df = web.DataReader(stock, self.data_source, begin_date, end_date)

    def calculateMA(self):
        self.df['Ma20'] = self.df.Close.rolling(window=20).mean()
        self.df['Ma30'] = self.df.Close.rolling(window=30).mean()
        self.df['Ma60'] = self.df.Close.rolling(window=60).mean()




if __name__ == '__main__':
    cvr = Stock()
    cvr.collectData('600797')
    print(cvr.df)
