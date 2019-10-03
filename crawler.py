#coding=utf-8
import requests, json
import pandas as pd
import numpy as np
import datetime
import math

if __name__ == '__main__':
    base_day = datetime.datetime(2009, 1, 3)
    price_data = pd.DataFrame(columns=[
        'tickertime', 'openprice', 'closeprice', 'high', 'low', 'predictprice'
    ])

    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    pages = range(1, 8)
    count = 0
    for page in pages:
        url = 'http://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=20090829&endtime=20291230&page={}&per_page=1000&webp=1'.format(
            page)
        web_data = requests.get(url, headers=header)
        web_data.encoding = 'utf-8'
        json_obj = json.loads(web_data.text)
        list_data = json_obj.get("data").get("list")

        for item in list_data:
            date = item.get("tickertime")[0:10]
            diff = datetime.datetime.strptime(date, '%Y-%m-%d') - base_day
            # predictPrice = (diff.days/693)**5.526
            predictPrice2 = 10**(-17.01593313 +
                                 5.84509376 * math.log10(diff.days))
            row = np.array([
                date,
                item.get("openprice"),
                item.get("closeprice"),
                item.get("high"),
                item.get("low"), predictPrice2
            ])
            price_data.loc[count] = row
            count = count + 1

    price_data.to_csv("price.csv", index=False, sep=',')
