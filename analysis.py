#coding=utf-8
import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
from pyecharts.charts import Line, Candlestick, Bar, Tab
import pyecharts.options as opts
import datetime


def close_ratio(close, base):
    return close * 1.0 / base


if __name__ == '__main__':
    price_data = pd.read_csv('price.csv',
                             index_col=0,
                             parse_dates=False,
                             infer_datetime_format=True)

    price_data = price_data.sort_index(axis=0, ascending=True)

    price_data['Candle_Data'] = price_data.apply(
        lambda x: [x['openprice'], x['closeprice'], x['low'], x['high']],
        axis=1)

    ma_list = [100, 200]

    for ma in ma_list:
        ma_str = str(ma)
        price_data['GMA_' + ma_str] = price_data['closeprice'].rolling(
            window=ma, min_periods=1).apply(gmean, raw=True)

    for ma in ma_list:
        ma_str = str(ma)
        price_data["GMA_Ratio_" + ma_str] = price_data.apply(
            lambda x: close_ratio(x['closeprice'], x['GMA_' + ma_str]), axis=1)

    price_data["Predict_Ratio"] = price_data.apply(
        lambda x: close_ratio(x['closeprice'], x['predictprice']), axis=1)

    time = price_data.index.tolist()

    candle = Candlestick()
    candle.add_xaxis(time).set_series_opts(type='time')
    candle.add_yaxis("日K", price_data['Candle_Data'].tolist())

    line1 = Line()
    line1.add_xaxis(time).set_series_opts(type='time')
    for ma in ma_list:
        ma_str = str(ma)
        line1.add_yaxis("GMA_" + ma_str,
                        price_data['GMA_' + ma_str].tolist(),
                        yaxis_index=0,
                        is_symbol_show=False)

    line2 = Line()
    line2.add_xaxis(time).set_series_opts(type='time')
    for ma in ma_list:
        ma_str = str(ma)
        line2.add_yaxis("GMA_Ratio_" + ma_str,
                        price_data['GMA_Ratio_' + ma_str].tolist(),
                        yaxis_index=1,
                        is_symbol_show=False)

    line2.add_yaxis("Predict_Ratio",
                    price_data['Predict_Ratio'].tolist(),
                    yaxis_index=1,
                    is_symbol_show=False)
    line2.set_series_opts(markline_opts=opts.MarkLineOpts(
        precision=2,
        is_silent=True,
        data=[
            opts.MarkLineItem(y=1.2),
            opts.MarkLineItem(y=1),
            opts.MarkLineItem(y=0.8),
        ],
        linestyle_opts=opts.LineStyleOpts(width=1, type_='dashed'),
        label_opts=opts.LabelOpts(is_show=True, position='middle')))

    line3 = Line()
    line3.add_xaxis(time).set_series_opts(type='time')
    line3.add_yaxis('Predict',
                    price_data['predictprice'].tolist(),
                    yaxis_index=0,
                    is_symbol_show=False)

    line1.extend_axis(yaxis=opts.AxisOpts())

    line1.set_global_opts(
        title_opts=opts.TitleOpts(title="Bitcoin"),
        xaxis_opts=opts.AxisOpts(type_="category", name="x"),
        yaxis_opts=opts.AxisOpts(
            type_="log",
            splitline_opts=opts.SplitLineOpts(is_show=False),
            is_scale=True,
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", trigger_on="mousemove"),
        datazoom_opts=[
            opts.DataZoomOpts(xaxis_index=0, range_start=80, range_end=100)
        ],
        visualmap_opts=opts.VisualMapOpts(
            min_=0.6,
            max_=2,
            pos_top=30,
            pos_right=0,
            split_number=100,
            series_index=[3, 4, 5],
            range_color=["red", "yellow", "orange", "green", "blue"],
            out_of_range={'color': '#999999'}),
    )

    line1.overlap(line3)
    line1.overlap(line2)
    line1.overlap(candle)

    ratio_columns = ['GMA_Ratio_100', 'GMA_Ratio_200', 'Predict_Ratio']
    threshold_level = [0, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 10000]
    data = {}
    for column in ratio_columns:
        series = price_data[column]
        totalCount = series.count()
        arr = []
        for index in range(len(threshold_level) - 1):
            min = threshold_level[index]
            max = threshold_level[index + 1]
            partial_data = price_data.loc[(price_data[column] >= min) &
                                          (price_data[column] < max), [column]]
            percentage = partial_data.count() / totalCount
            arr.append(percentage[column])
        data[column] = arr

    bar_xaxis = [
        "[0,0.6)", "[0.6,0.8)", "[0.8,1)", "[1,1.2)", "[1.2,1.4)", "[1.4,1.6)",
        "[1.6,1.8)", "[1.8,2)", "[2,...)"
    ]
    bar = Bar()
    bar.add_xaxis(bar_xaxis)
    bar.add_yaxis("GMA_Ratio_100", data["GMA_Ratio_100"])
    bar.add_yaxis("GMA_Ratio_200", data["GMA_Ratio_200"])
    bar.add_yaxis("Predict_Ratio", data["Predict_Ratio"])
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    # line1.render("chart.html")

    # page = Page()
    # page.add(line1, bar)
    # page.render("chart.html")

    tab = Tab()
    tab.add(line1, "overall")
    tab.add(bar, "ratio distribution")
    tab.render("chart.html")
