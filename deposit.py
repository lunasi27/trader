import pandas as pd


class Deposit():
    def __init__(self, stock_df):
        self.stock_df = stock_df
        self.cach_hold = 0
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
        else:
        #Strategy buy
            pass

    def sell(self, date, number=None): 
        #All out sell
        if number is None:
            if self.posit_num is 0:
                return
            #Use '0' stand for sell signal
            self.stock_df.loc[date, 'Signal'] = 0
            self.stock_df.loc[date, 'Price'] = price
            self.cach_hold += price * self.posit_num
            self.posit_num = 0
        else:
        # Strategy sell
            pass

    def summary(self):
        for idx,today in self.stock_df.iterrow():
            if today.Signal == 1:
                #Buy
                self.buy(idx, today.Price)
            elif today.Signal == 0:
                #Sell
                self.sell(idx, today.Price)
            #Save market_total
            if self.posit_num is 0:
                self.stock_df.loc[idx, 'Total'] = self.cach_hold
            else:
                market_total = today.Price * self.posit_num + self.cach_hold
                self.stock_df.loc[idx, 'Total'] = market_total
                
