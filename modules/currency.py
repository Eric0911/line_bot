from pyquery import PyQuery
import requests
import moment

#取得匯率
def get_exchange_table():
    # 資料來源網址
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    # 輸出的字典
    table = {}
    # 爬取整份網頁
    res = requests.get(url)
    html = res.text
    html = PyQuery(html)
    # 所有貨幣名稱
    names = html('div.hidden-phone.print_show').text().split()
    # 所有現金買價
    buy_list = html(
        'td.rate-content-cash.text-right.print_hide[data-table="本行現金買入"]').text().split()
    # 所有現金賣價
    sell_list = html(
        'td.rate-content-cash.text-right.print_hide[data-table="本行現金賣出"]').text().split()
    # 價格計數器
    p = 0
    for n_idx, name in enumerate(names):
        if n_idx % 2 == 0:
            table[name] = {
                "buy": buy_list[p],
                "sell": sell_list[p]
            }
            # 把p+1
            p += 1
    print(table)
    return table

#取得股價
def get_stock_info():
    stock_id_list = ["2330", "2317", "0050", "2454", "2412", "0056"]
    # url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw&json=1&delay=0"
    param_list = []
    for stock_id in stock_id_list:
        param_list.append(f"tse_{stock_id}.tw")
    # print(param_list)
    param = "|".join(param_list)
    # print(param)
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={param}&json=1&delay=0"
    # print(url)
    res = requests.get(url)
    data = res.json()["msgArray"]
    stock_list = {}
    # 取出證交所提供的所有個股資料
    for d in data:
        try:
            # 個股最新成交價 轉為浮點數
            price = float(d["z"])
            # 相減後四捨五入到小數點第2位
            change = round( price - float(d["y"]), 2)
            origin_time = d["d"] + " " + d["t"]
            date = moment.date(origin_time, "YYYYMMDD HH:mm:ss").format("YYYY/MM/DD HH:mm:ss")
            name = d["n"]
            stock_list[name] = {
                "id": d["c"],
                "price": price,
                "change": change,
                "volume": int(d["v"]),
                "date": date
            }
        except:
            # 如果 try 中有錯誤...
            print(f"處理錯誤資料: {d}")
            
    result = stock_list
    print(result)

    return result