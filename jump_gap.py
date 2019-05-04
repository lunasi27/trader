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
    def __init__(self, df_obj):
        self.stock_df = df_obj

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


class DrawGap(KCurve):
    def __init__(self):
        super(drawGap, self).__init__()

    def show(self, stock_df, jump_df):
        self.setData(stock_df)
        pass


class FilterGap(JumpGap, DrawGap):
    def __init__(self, df_obj, kav_obj):
        super(FilterGap, self).__init__(df_obj)
        self.draw_gap = DrawGap()
        

    def findGap(self):
        df_gap = self.calculate()
        df_gap = df_gap[(np.abs(df_gap.changeRatio)>3)&(df_gap.Volume>df_gap.Volume.median())]
        return df_gap

    def show(self, df):
        print(df.filter(['jump_power', 'preClose', 'changeRatio', 'Close', 'Volume']))



if __name__ == '__main__':
    sd = Stock()
    sd.collectData('600797')
    jump_gap_obj = FilterGap(sd.df)
    gaps = jump_gap_obj.findGap()
    jump_gap_obj.show(gaps)
