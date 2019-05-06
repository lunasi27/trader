import codecs
import csv
import numpy as np
from data import Stock
import pdb


class Deposit():
    def __init__(self, stock_df):
        self.stock_df = stock_df
        self.cach_hold = 10000
        self.market_total = 0
        self.posit_num = 0
        self.profit_curve = []

    def buy(self, date, price, number=None):
        #All in buy
        if number is None:
            #Use '1' stand for buy signal
            self.stock_df.loc[date, 'Signal'] = 1
            self.stock_df.loc[date, 'Price'] = price
            buy_posit = int(self.cach_hold / price)
            self.cach_hold -= price * buy_posit
            self.posit_num += buy_posit
            #Update Total deposition
            market_total = price * self.posit_num + self.cach_hold
            self.stock_df.loc[date, 'Total'] = market_total
        else:
        #Strategy buy
            pass

    def sell(self, date, price, number=None): 
        #All out sell
        if number is None:
            if self.posit_num is 0:
                return
            #Use '0' stand for sell signal
            self.stock_df.loc[date, 'Signal'] = 0
            self.stock_df.loc[date, 'Price'] = price
            self.cach_hold += price * self.posit_num
            self.posit_num = 0
            #Update Total deposition
            self.stock_df.loc[date, 'Total'] = self.cach_hold
        else:
        # Strategy sell
            pass

    def summary(self):
        self.stock_df['BenchmarkProfit'] = np.log(self.stock_df.Close/self.stock_df.Close.shift(1))
        for idx,today in self.stock_df.iterrows():
            pass
            #Save market_total
        print('Cache: %s' % self.cach_hold)
        #print('Market: %s' % )
        #print('Total: %s' % )
                

    def mark(self):
        with codecs.open('./zdwx.csv') as fd:
            reader = csv.DictReader(fd)
            rows = [row for row in reader]
        for row in rows:
            buy_date = row['买入时间']
            buy_price = row['买入价']
            sell_date = row['卖出时间']
            sell_price = row['卖出价']
            hands_num = row['股数']
            self.buy(buy_date, float(buy_price))
            self.sell(sell_date, float(sell_price))

        

if __name__ == '__main__':
    ss = Stock()
    ss.collectData('600797')
    dd = Deposit(ss.df)
    dd.mark()
    dd.summary()
