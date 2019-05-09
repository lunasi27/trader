import numpy as np
from data import Stock
from graph import KCurve
import pdb


class Cross():
    def __init__(self, stock, graph):
        self.df = stock.df
        self.graph = graph
        self.graph.setData(self.df)
        self.graph.candle()
        self.graph.average()

    def calculate(self):
        list_diff = np.sign(self.df['ma20']-self.df['ma30'])
        list_signal = np.sign(list_diff - list_diff.shift(1))
        for idx in range(len(list_signal)):
            if list_signal[idx] < 0:
                # print
                print('Bad cross')
                self.graph.plt_KAV.annotate(u"死叉", xy=(idx, self.df['ma20'][idx]), xytext=(idx, self.df['ma20'][idx]+1.5), arrowprops=dict(facecolor='green', shrink=0.2))
                print(self.df.iloc[idx])
            elif list_signal[idx] > 0:
                # print
                print('Good cross')
                self.graph.plt_KAV.annotate(u"金叉", xy=(idx, self.df['ma20'][idx]), xytext=(idx, self.df['ma20'][idx]-1.5), arrowprops=dict(facecolor='red', shrink=0.2))
                print(self.df.iloc[idx])
            else:
                pass

    def show(self):
        self.graph.show()


if __name__ == '__main__':
    stock = Stock()
    stock.collectData('600797')
    stock.calculateMA()
    cvr = KCurve()
    cross = Cross(stock, cvr)
    cross.calculate()
    cross.show()
