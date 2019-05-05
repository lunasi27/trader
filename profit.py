import csv
import codecs
from graph import KCurve
from data import Stock
import pdb


if __name__ == '__main__':
    stock = Stock()
    stock.collectData('600797')
    
    with codecs.open('./zdwx.csv') as fd:
        data_dict = csv.DictReader(fd)
        rows = [row for row in data_dict]
    for row in rows:
        buy_date = row['买入时间']
        sell_date = row['卖出时间']
        print('buy_date = %s, sell_date = %s' % (buy_date, sell_date))
    stock.df.index.get_loc(tt)
