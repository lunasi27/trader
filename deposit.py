import codecs
import csv
import numpy as np
from data import Stock
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pdb


class Deposit():
    def __init__(self, stock_df):
        self.stock_df = stock_df
        self.cash = 10000
        self.market_cap = 0
        self.profit_curve = []
        #Initial cash
        self.stock_df.loc[self.stock_df.index[0], 'Cash'] = self.cash
        self.total = 0

    def buy(self, date, price, number=None):
        #All in buy
        if number is None:
            #Update buy price and hold position
            self.stock_df.loc[date, 'Price'] = price
            buy_posit = int(self.cash / price)
            self.stock_df.loc[date, 'Hold'] = buy_posit
            #Update cash
            cash = self.stock_df.Cash.asof(date)
            cash -= price * buy_posit
            assert cash > 0
            self.stock_df.loc[date, 'Cash'] = cash
            #Update market cap
            posit_num = self.stock_df.Hold.sum()
            assert posit_num > 0
            self.stock_df.loc[date, 'MarketCap'] = price * posit_num
        else:
        #Strategy buy
            pass

    def sell(self, date, price, number=None): 
        #All out sell
        if number is None:
            posit_num = self.stock_df.Hold.sum()
            assert posit_num >= 0
            if posit_num is 0:
                return
            #Update sell price and hold position
            self.stock_df.loc[date, 'Price'] = price
            self.stock_df.loc[date, 'Hold'] = -posit_num
            # Update cash
            cash = self.stock_df.Cash.asof(date)
            cash += price * posit_num
            #Update Total deposition
            self.stock_df.loc[date, 'Cash'] = cash
            #Refresh current hold positon
            posit_num = self.stock_df.Hold.sum()
            assert posit_num == 0
            self.stock_df.loc[date, 'MarketCap'] = price * posit_num
        else:
        # Strategy sell
            pass

    def getKeep(self):
        keep = self.stock_df.Hold.copy()
        keep[keep>0] = 1
        keep[keep<0] = 0
        keep.fillna(method='ffill', inplace=True)
        keep.fillna(0, inplace=True)
        return keep

    def refresh(self):
        # Profit
        self.stock_df['BenchmarkProfit'] = np.log(self.stock_df.Close/self.stock_df.Close.shift(1))
        self.stock_df.BenchmarkProfit.fillna(0, inplace=True)
        keep = self.getKeep()
        self.stock_df['TrendProfit'] = keep * self.stock_df.BenchmarkProfit
        # Total
        self.stock_df.Cash.fillna(method='ffill', inplace=True)
        self.stock_df.MarketCap.fillna(method='ffill', inplace=True)
        self.stock_df.MarketCap.fillna(0, inplace=True)
        self.total = self.stock_df.Cash + self.stock_df.MarketCap
        #print('Total: %s' % total)

    def applyOperate(self):
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

    def view(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(figsize=(8,6), dpi=100, facecolor='white')
        gs = gridspec.GridSpec(3, 1, left=0.05, bottom=0.15, right=0.96, top=0.96, wspace=None, hspace=0.2, height_ratios=[4.5, 2, 2])
        graph_trade = fig.add_subplot(gs[0, :])
        graph_total = fig.add_subplot(gs[1, :])
        graph_profit = fig.add_subplot(gs[2, :])
        for idx,today in self.stock_df.iterrows():
            if today.Hold > 0:
                start = self.stock_df.index.get_loc(idx)
                hands_num = today.Hold
            if today.Hold < 0:
                end = self.stock_df.index.get_loc(idx)
                if self.stock_df.Close[end] < self.stock_df.Close[start]:
                    graph_trade.fill_between(self.stock_df.index[start:end],0,self.stock_df.Close[start:end],color='green',alpha=0.38)
                    is_win = False
                else:
                    graph_trade.fill_between(self.stock_df.index[start:end],0,self.stock_df.Close[start:end],color='red',alpha=0.38)
                    is_win = True
                graph_trade.annotate('获利\n%s手' % hands_num if is_win else '亏损\n%s手' % hands_num, xy=(idx,self.stock_df.Close.asof(idx)), xytext=(idx, self.stock_df.Close.asof(idx)+4), arrowprops=dict(facecolor='yellow',shrink=0.1), horizontalalignment='left', verticalalignment='top')
        graph_trade.plot(self.stock_df.index,self.stock_df.Close,color='r')
        graph_trade.fill_between(self.stock_df.index,0,self.stock_df.Close,color='blue',alpha=.08)
        graph_trade.set_ylabel('close')
        graph_trade.set_title(u'浙大网新')
        graph_trade.grid(True)
        #graph_trade.set_xlim(0,len(self.stock_df.index))
        #graph_trade.set_xticks(range(0,len(self.stock_df.index),20))
        graph_trade.set_ylim(np.min(self.stock_df.Close)-5,np.max(self.stock_df.Close)+5)#设置Y轴范围
        graph_trade.legend(['Close'],loc='best')
        # Total
        self.total.plot(grid=True, ax=graph_total)
        #graph_total.set_xlim(0,len(self.stock_df.index))
        #graph_total.set_xticks(range(0,len(self.stock_df.index),20))
        graph_total.legend(['total'], loc='best')
        # profit
        self.stock_df[['BenchmarkProfit','TrendProfit']].cumsum().plot(grid=True, ax=graph_profit)
        graph_profit.set_xlabel('time')
        graph_profit.legend(['BenchmarkProfit','TrendProfit'], loc='best')
        #graph_profit.set_xlim(0,len(self.stock_df.index))
        #graph_profit.set_xticks(range(0,len(self.stock_df.index),20))
        # show now
        plt.show()
        

if __name__ == '__main__':
    ss = Stock()
    ss.collectData('600797')
    dd = Deposit(ss.df)
    dd.applyOperate()
    dd.refresh()
    dd.view()
