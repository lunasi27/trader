import datetime
import numpy as np
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import matplotlib.gridspec as gridspec
import pdb
from data import Stock
from graph import KCurve


class JumpGap():
    def __init__(self, stock):
        self.stock_df = stock.df

    def calculate(self):
        self.gap_df = pd.DataFrame()
        jump_threshold = self.stock_df.Close.median() * 0.01
        self.stock_df['preClose'] = self.stock_df.Close.shift(1)
        self.stock_df['changeRatio'] = self.stock_df.Close.pct_change() * 100
        for idx in np.arange(0, self.stock_df.shape[0]):
            today =  self.stock_df.iloc[idx].copy()
            if (today.changeRatio > 0) and ((today.Low - today.preClose) > jump_threshold):
                today['jump_power'] = (today.Low - today.preClose) / jump_threshold
                self.gap_df = self.gap_df.append(today)
            elif (today.changeRatio < 0) and ((today.preClose - today.High) > jump_threshold):
                today['jump_power'] = (today.High - today.preClose) / jump_threshold
                self.gap_df = self.gap_df.append(today)
            else:
                pass
        #return jump_df


class DrawGap():
    def __init__(self, graph_obj):
        self.graph = graph_obj

    def addMark(self, jump_df):
        stock_df = self.graph.df
        for idx in np.arange(0, jump_df.shape[0]):
            today = jump_df.iloc[idx]
            inday = stock_df.index.get_loc(jump_df.index[idx])
            if today['jump_power'] > 0:
                self.graph.plt_KAV.annotate('up',xy=(inday,today.Low*0.95),xytext=(inday, today.Low*0.9),arrowprops=dict(facecolor='red',shrink=0.01),horizontalalignment='left',verticalalignment='top')
            elif today['jump_power'] < 0:
                self.graph.plt_KAV.annotate('down',xy=(inday,today.High*1.05),xytext=(inday, today.High*1.1),arrowprops=dict(facecolor='green',shrink=0.01),horizontalalignment='left',verticalalignment='top')



class FindGap(JumpGap):
    def __init__(self, stock_obj, graph_obj):
        super(FindGap, self).__init__(stock_obj)
        self.draw_gap = DrawGap(graph_obj)

    def calculate(self):
        super(FindGap, self).calculate()
        self.selected_gap = self.gap_df[(np.abs(self.gap_df.changeRatio)>3)&(self.gap_df.Volume>self.gap_df.Volume.median())]
        #return selected_gap

    def show(self):
        print(self.selected_gap.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))
        self.draw_gap.graph.setData(self.stock_df)
        self.draw_gap.graph.candle()
        self.draw_gap.addMark(self.selected_gap)
        self.draw_gap.graph.show()
        



if __name__ == '__main__':
    stock = Stock()
    stock.collectData('600797')
    kav = KCurve()
    jump_gap = FindGap(stock, kav)
    jump_gap.calculate()
    jump_gap.show()
