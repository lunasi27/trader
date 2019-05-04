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
    def __init__(self, stock_df):
        self.stock_df = stock_df

    def calculate(self):
        jump_df = pd.DataFrame()
        jump_threshold = self.stock_df.Close.median() * 0.01
        self.stock_df['preClose'] = self.stock_df.Close.shift(1)
        self.stock_df['changeRatio'] = self.stock_df.Close.pct_change() * 100
        for idx in np.arange(0, self.stock_df.shape[0]):
            today =  self.stock_df.iloc[idx].copy()
            if (today.changeRatio > 0) and ((today.Low - today.preClose) > jump_threshold):
                today['jump_power'] = (today.Low - today.preClose) / jump_threshold
                jump_df = jump_df.append(today)
            elif (today.changeRatio < 0) and ((today.preClose - today.High) > jump_threshold):
                today['jump_power'] = (today.High - today.preClose) / jump_threshold
                jump_df = jump_df.append(today)
            else:
                pass
        return jump_df


class DrawGap():
    def __init__(self, graph_obj):
        self.graph = graph_obj

    def addMark(self, stock_df, jump_df):
        for idx in np.arange(0, jump_df.shape[0]):
            today = jump_df.iloc[idx]
            inday = stock_df.index.get_loc(jump_df.index[idx])
            if today['jump_power'] > 0:
                self.graph.plt_KAV.annotate('up',xy=(inday,today.Low*0.95),xytext=(inday, today.Low*0.9),arrowprops=dict(facecolor='red',shrink=0.01),horizontalalignment='left',verticalalignment='top')
            elif today['jump_power'] < 0:
                self.graph.plt_KAV.annotate('down',xy=(inday,today.High*1.05),xytext=(inday, today.High*1.1),arrowprops=dict(facecolor='green',shrink=0.01),horizontalalignment='left',verticalalignment='top')



class FindGap():
    def __init__(self, stock_obj, graph_obj):
        self.jump_gap = JumpGap(stock_obj.df)
        self.draw_gap = DrawGap(graph_obj)

    def calculate(self):
        selected_gap = self.jump_gap.calculate()
        selected_gap = selected_gap[(np.abs(selected_gap.changeRatio)>3)&(selected_gap.Volume>selected_gap.Volume.median())]
        self.gap_df = selected_gap
        #return selected_gap

    def show(self):
        print(self.gap_df.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))
        self.draw_gap.graph.setData(stock_df)
        self.draw_gap.graph.candle()
        self.draw_gap.addMark(self.jump_gap.stock_df, self.gap_df)
        self.draw_gap.graph.show()
        



if __name__ == '__main__':
    stock = Stock()
    stock.collectData('600797')
    kav = KCurve()
    jump_gap = FindGap(stock, kav)
    jump_gap.calculate()
    jump_gap.show()
