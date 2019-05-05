import csv
import codecs
from graph import KCurve
from data import Stock
import pdb
import numpy as np
import matplotlib.pyplot as plt


class Profit():
    def __Init__(self):
        pass

    def setData(self, stock_name):
        self.stock = Stock()
        self.stock.collectData(stock_name)
        self.df = self.stock.df
        # Collect operations
        with codecs.open('./zdwx.csv') as fd:
            reader = csv.DictReader(fd)
            rows = [row for row in reader]
        for row in rows:
            buy_date = row['买入时间']
            sell_date = row['卖出时间']
            hands_num = row['股数']
            start = self.df.index.get_loc(buy_date)
            end = self.df.index.get_loc(sell_date)
            # Begin drawn
            if self.df.Close[end] < self.df.Close[start]:
                plt.fill_between(self.df.index[start:end], 0, self.df.Close[start:end], color='green', alpha=0.38)
                is_win = False
            else:
                plt.fill_between(self.df.index[start:end], 0, self.df.Close[start:end], color='red', alpha=0.38)
                is_win = True
            plt.annotate('获利'+hands_num+u'手' if is_win else '亏损\n'+hands_num+u'手',xy=(sell_date,self.df.Close.asof(sell_date)),xytext=(sell_date,self.df.Close.asof(sell_date)+4),arrowprops=dict(facecolor='yellow',shrink=0.1),horizontalalignment='left',verticalalignment='top')
            print('buy_date = %s, sell_date = %s' % (buy_date, sell_date))

    def show(self):
        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
        plt.plot(self.df.index, self.df.Close, color='r')
        plt.xlabel('time')
        plt.ylabel('close')
        plt.title(u'浙大网新')
        plt.grid(True)
        plt.ylim(np.min(self.df.Close)-5, np.max(self.df.Close)+5)
        plt.legend(['Close'], loc='best')
        plt.show()

            


if __name__ == '__main__':
    prof = Profit()
    prof.setData('600797')
    prof.show()
