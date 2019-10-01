#coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import gmean
from pyecharts.charts import Line, Candlestick
import pyecharts.options as opts

def close_ratio(close, base):
    return close*1.0/base

if __name__ == '__main__':
    price_data = pd.read_csv('price.csv', index_col=0, parse_dates=True, infer_datetime_format=True)
    ma_list = [100, 200]

    for ma in ma_list:
        ma_str = str(ma)
        price_data['GMA_'+ ma_str] = price_data['closeprice'].rolling(window=ma, center=True, min_periods=1).apply(gmean, raw=True)  

    
    for ma in ma_list:
        ma_str = str(ma)
        price_data["GMA_Ratio_"+ma_str] = price_data.apply(lambda x: close_ratio(x['closeprice'],x['GMA_'+ma_str]), axis = 1)

    price_data['Candle_Data'] = price_data.apply(lambda x: [x['openprice'], x['closeprice'], x['low'], x['high']], axis = 1)

    price_data = price_data.sort_index(axis=0, ascending=True)

    time = price_data.index.tolist()

    candle = Candlestick()
    candle.add_xaxis(time).set_series_opts(type='time')
    candle.add_yaxis("data", price_data['Candle_Data'].tolist())

    line1 = Line()

    line1.add_xaxis(time).set_series_opts(type='time')
    for ma in ma_list:
        ma_str = str(ma)
        line1.add_yaxis("GMA_"+ma_str,price_data['GMA_'+ma_str].tolist(),yaxis_index=0, is_symbol_show=False)

    line2 = Line()
    line2.add_xaxis(time).set_series_opts(type='time')
    for ma in ma_list:
        ma_str = str(ma)
        line2.add_yaxis("GMA_Ratio_"+ma_str,price_data['GMA_Ratio_'+ma_str].tolist(),yaxis_index=1, is_symbol_show=False)

    line1.extend_axis(yaxis=opts.AxisOpts())
    candle.extend_axis(yaxis=opts.AxisOpts())

    line1.set_global_opts(
        title_opts=opts.TitleOpts(title="Line-基本示例"),
        xaxis_opts=opts.AxisOpts(type_="category", name="x"),
        yaxis_opts=opts.AxisOpts(
            # type_="log",
            splitline_opts=opts.SplitLineOpts(is_show=True), 
            is_scale=True,),
        tooltip_opts=opts.TooltipOpts(trigger="axis", trigger_on="mousemove"),
        datazoom_opts=[
            opts.DataZoomOpts(xaxis_index=0, range_start=80, range_end=100)
        ],)
    
    line1.overlap(line2)
    line1.overlap(candle)
         
    line1.render("chart.html")