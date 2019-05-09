import datetime
import numpy as np
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import matplotlib.gridspec as gridspec

from data import Stock
import pdb


#plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class KCurve():
    def __init__(self):
        self.fig = plt.figure(figsize=(8,6), dpi=100, facecolor="white")
        self.fig.subplots_adjust(left=0.09, bottom=0.20, right=0.94, 
                                 top=0.90, wspace=0.2, hspace=0)
        self.gs = gridspec.GridSpec(2, 1, left=0.05, bottom=0.15, right=0.96,
                                    top=0.96, wspace=None, hspace=0,
                                    height_ratios=[3.5,1])

    def show(self):
        plt.show()

    def setData(self, stock_df):
        self.df = stock_df

    def candle(self):
        #self.plt_KAV = self.fig.add_subplot(1,1,1)
        self.plt_KAV = self.fig.add_subplot(self.gs[0,:])
        self.plt_KAV.set_title(u"600797 浙大网新-日K线")
        self.plt_KAV.set_xlabel(u"日期")
        self.plt_KAV.set_ylabel(u"价格")
        self.plt_KAV.set_xlim(0,len(self.df.index)) 
        self.plt_KAV.set_xticks(range(0,len(self.df.index),15))
        self.plt_KAV.grid(True,color='k')
        pdb.set_trace()
        self.plt_KAV.set_xticklabels([self.df.index.strftime('%Y-%m-%d')[index]
                                     for index in self.plt_KAV.get_xticks()])
        for label in self.plt_KAV.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)
        mpf.candlestick2_ochl(self.plt_KAV, self.df.open, self.df.close,
                              self.df.high, self.df.low, width=0.5, colorup='r',
                              colordown='g')

    def average(self):
        numt = np.arange(0, len(self.df.index)) 
        self.plt_KAV.plot(numt, self.df['ma20'],'black',label='M20',lw=1.0)
        self.plt_KAV.plot(numt, self.df['ma30'],'green',label='M30',lw=1.0)
        self.plt_KAV.plot(numt, self.df['ma60'],'blue',label='M60',lw=1.0)
        self.plt_KAV.legend(loc='best') 

    def volumn(self):
        self.plt_VOL = self.fig.add_subplot(self.gs[1,:])
        numt = np.arange(0, len(self.df.index)) 
        self.plt_VOL.bar(numt, self.df.volume, color=['g' if self.df.open[x] > self.df.close[x] else 'r' for x in range(0,len(self.df.index))])
        self.plt_VOL.set_ylabel(u"成交量")
        self.plt_VOL.set_xlabel(u"日期")
        self.plt_VOL.set_xlim(0,len(self.df.index)) 
        self.plt_VOL.set_xticks(range(0,len(self.df.index), 15))
        self.plt_VOL.set_xticklabels([self.df.index.strftime('%Y-%m-%d')[index] for index in self.plt_VOL.get_xticks()])
        for label in self.plt_KAV.xaxis.get_ticklabels():
            label.set_visible(False)
        for label in self.plt_VOL.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)

    def macd(self):
        pass

    def kjd(self):
        pass



if __name__ == '__main__':
    stock = Stock()
    stock.collectData('600797')
    stock.calculateMA()
    cvr = KCurve()
    cvr.setData(stock.df)
    cvr.candle()
    cvr.average()
    cvr.volumn()
    cvr.show()
