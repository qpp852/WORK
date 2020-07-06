# 載入套件
import requests
import numpy as np
import time
import datetime
import pandas as pd
from io import BytesIO, StringIO
from bs4 import BeautifulSoup as bs

# -------------------------------登入行將-------------------------------- #
# 使用session並網頁登入
session_requests = requests.session()
login_url = "https://www.sinjang.com.tw/Portal/"
result = session_requests.get(login_url)
soup = bs(result.text)

# 抓取csrf_token及其他request所需資料
viewstate = soup.find(id="__VIEWSTATE")['value']
viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
validation = soup.find(id="__EVENTVALIDATION")['value']

# 輸入post的param及header
payload = {
    'ctl00$ScriptManager1': 'ctl00$BodyContent$AjaxPanel|ctl00$BodyContent$LOGIN_BTN',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    '__VIEWSTATEENCRYPTED': '',
    '__EVENTVALIDATION': validation,
    'ctl00$BodyContent$H_MONTH': '10',
    'ctl00$BodyContent$H_YEAR': '2019',
    'ctl00$BodyContent$monthflag': '',
    'ctl00$BodyContent$H_HAPPY_URL': 'http://fun.sinjang.com.tw/',
    'ctl00$BodyContent$hidCOUNTDOWN': '',
    'ctl00$BodyContent$hidALERTTIME': '',
    'ctl00$BodyContent$hidTIMEFLAG': '',
    'ctl00$BodyContent$timer_idx': '',
    'ctl00$BodyContent$ACCOUNT': 'K914',
    'ctl00$BodyContent$PASSWORD': '80305460',
    '__ASYNCPOST': 'true',
    'ctl00$BodyContent$LOGIN_BTN.x': '36',
    'ctl00$BodyContent$LOGIN_BTN.y': '61'
}

header = {
    'Host': 'www.sinjang.com.tw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.sinjang.com.tw/Portal/AUC2101_.aspx',
    'X-MicrosoftAjax': 'Delta=true',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'Content-Length': '14209',
    'Connection': 'keep-alive',
}

# 完成登入，並將登入後頁面存入result中
result = session_requests.post(
    login_url,
    data=payload,
    headers=header
)

# 檢視是否登入成功
# bs(result.text)


# -----------------------------完成登入後爬取資料-------------------------- #
# 登入成功後使用同一個session去爬取我們需要的頁面
crw_url = 'https://www.sinjang.com.tw/Portal/BA0102_01.aspx'
crw_result = session_requests.get(crw_url)

# 抓取csrf_token及其他request所需資料
crw_soup = bs(crw_result.text)
crw_viewstate = crw_soup.find(id="__VIEWSTATE")['value']
crw_viewstategenerator = crw_soup.find(id="__VIEWSTATEGENERATOR")['value']
crw_pageid = crw_soup.find(id="PAGE_ID")['value']
crw_validation = crw_soup.find(id="__EVENTVALIDATION")['value']

# 輸入爬取參數 : 交易時間
BID_DATE_S = input('Start_date : yyyy/m/d \n')
BID_DATE_S_F = datetime.datetime.strptime(BID_DATE_S, '%Y/%m/%d').strftime('%Y%m%d')
BID_DATE_E = input('End_date : yyyy/m/d \n')
BID_DATE_E_F = datetime.datetime.strptime(BID_DATE_E, '%Y/%m/%d').strftime('%Y%m%d')
# BRANDS = ['AUDI', 'PORSCHE', 'SKODA', 'VW']
BRANDS = ['05', '56', '64', '73']
maindf = pd.DataFrame()

for BRAND in BRANDS:
    # 輸入post的param及header
    crw_param = {
        'ScriptManager1': 'AjaxPanel|ReQuery',
        'ActivePageControl': 'PC2',
        'ColumnFilter': '',
        'M_PKNO': '',
        'Mode': 'ADD',
        'ROWSTAMP': '',
        'TYPE': '',
        'PASSWORD': '',
        'PASSWORD_C': '',
        'PAGE_ID': crw_pageid,
        'TAB': '1',
        'Q_BID_DATE_S': BID_DATE_S,
        'Q_BID_DATE_E': BID_DATE_E,
        'Q_BRAND_ID': BRAND,
        'Q_MODEL_ID': '',
        'Q_CAR_AGE_S': '',
        'Q_CAR_AGE_E': '',
        'Q_TOLERANCE_S': '',
        'Q_TOLERANCE_E': '',
        'Q_CAR_DOOR': '',
        'Q_OUTSIDE_POINT': '',
        'Q_WD': '',
        'Q_GEAR_TYPE': '',
        'PC$PageSize': '50',
        'PC$PageNo': '1',
        'PC2$PageSize': '99999',
        'PC2$PageNo': '1',
        '__EVENTTARGET': 'ReQuery',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': crw_viewstate,
        '__VIEWSTATEGENERATOR': crw_viewstategenerator,
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTVALIDATION': crw_validation,
        '__ASYNCPOST': 'true',
        #     'QUERY_BTN1' : '查  詢',
    }

    crw_header = {
        'Host': 'www.sinjang.com.tw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.sinjang.com.tw/Portal/BA0102_01.aspx',
        'X-MicrosoftAjax': 'Delta=true',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Content-Length': '8257',
        'Connection': 'keep-alive',
    }

    # 送出請求
    crw_result = session_requests.post(
        crw_url,
        data=crw_param,
        headers=crw_header
    )

    # 使用pandas讀取html
    table = pd.read_html(StringIO(crw_result.text))

    maindf = maindf.append(table[7])
    time.sleep(3)

column = ['拍賣日期', '頻道', '拍賣編號', '查看資料', '廠牌', '車型', '監理型式', '式樣', '排檔', '出廠年月', '排氣量', '顏色',
          '傳動方式', '車門', '車體評價', '內裝評價', '里程', '里程保證', '成交價', '牌照稅', '燃料費', '違規',
          '成交價(調整)', '排氣量(調整)']
maindf['拍賣日期'] = pd.to_datetime(maindf.拍賣日期)
maindf['成交價(調整)'] = maindf.成交價 + maindf.牌照稅 + maindf.燃料費 + maindf.違規
maindf['排氣量(調整)'] = np.ceil(maindf.排氣量 / 100) / 10
maindf['廠牌'] = maindf.廠牌車型.str.split(' ').apply(lambda x: x[0])
maindf['車型'] = maindf.廠牌車型.str.split(' ').apply(lambda x: x[2])
maindf.drop('廠牌車型', inplace=True, axis=1)
maindf[column].to_excel('C:\行將交易資料\行將_' + BID_DATE_S_F + '-' + BID_DATE_E_F + '.xlsx', index=False)
print('----------------------------------Finished----------------------------------------')