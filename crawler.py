#coding=utf-8
import requests, json
import pandas as pd
import numpy as np


if __name__ == '__main__':
    price_data = pd.DataFrame(columns=['tickertime', 'openprice', 'closeprice', 'high', 'low'])

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    pages = range(1, 8)
    count = 0
    for page in pages:
        url = 'http://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=20090829&endtime=20190928&page={}&per_page=1000&webp=1'.format(page)
        web_data = requests.get(url, headers=header)
        web_data.encoding = 'utf-8'
        json_obj = json.loads(web_data.text)
        list_data = json_obj.get("data").get("list")

        for item in list_data:
            row = np.array([item.get("tickertime"), item.get("openprice"),item.get("closeprice"),item.get("high"),item.get("low")])
            price_data.loc[count] = row
            count = count + 1
    
    price_data.to_csv("price.csv",index=False,sep=',')
