import requests
from bs4 import BeautifulSoup
import twstock
import requests
import schedule
import time
import re
import time
from interval import Interval

#關閉 ipv6

data = requests.get("https://tw.stock.yahoo.com/rank/volume")
soup = BeautifulSoup(data.text, "html.parser")
b_tag = soup.find_all(class_="Fz(14px) C(#979ba7) Ell")
list_b_tag = list(b_tag)

soup_val = BeautifulSoup(data.text, "html.parser")
b_tag_val = soup_val.find_all(class_="Jc(fe) Fw(600) D(f) Ai(c) C($c-trend-down)")
list_b_tag_val = list(b_tag_val)

max_idx = 0
now = 0
outside = 0
category_name = []
category_name1 = []
stock_num = 15

def get_two_float(f_str, n):
    a, b, c = f_str.partition('.')
    c = c[:n]
    return ".".join([a, c])
# 把回傳數字保留小數後兩位的function

def containEnglish(str0):
    return bool(re.search('[A-Z]',str0))

def get_column(target_day1,from_day2):
    capacity_1 = int((stock1.moving_average(stock1.capacity, target_day1)[-1]) / 1000)
    capacity_2 = int((stock1.moving_average(stock1.capacity, from_day2)[-1]) / 1000)
    return (capacity_1 * target_day1) - (capacity_2 * from_day2)

def rfi_state():
    all_RSI = 0
    RSI_DAY = 5
    negative = 0
    RSI = 0
    for RSI_COUNT in range(1, RSI_DAY + 1):
        print(RSI_COUNT)
        if stock1.change[-RSI_COUNT] > 0:
            all_RSI = stock1.change[-RSI_COUNT] + all_RSI

        else:
            negative = abs(stock1.change[-RSI_COUNT]) + negative

    RSI = ((all_RSI / RSI_DAY) / ((all_RSI / RSI_DAY) + (negative / RSI_DAY))) * 100
    print(RSI)

for i in range(stock_num):
    list_b_tag1 = str(list_b_tag[i])
    after_sp = list_b_tag1.split('">')[-1].split('.TW')[0] #去切文字，利用符號切其中-1是後面數回來的位置
    category_name.append(after_sp) #將中文目錄丟入list中





old_stock_id = 0
now_localtime_set_hstart = 9
now_localtime_set_hstop = 24
now_localtime_set_mstart1 = 1
now_localtime_set_mstop1 = 30
now_localtime_set_mstart2 = 30
now_localtime_set_mstop2 = 59



while 1:
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    if int(now_localtime.split(":")[0]) >= now_localtime_set_hstart and int(now_localtime.split(":")[0]) <= now_localtime_set_hstop : #切字元
        if int(now_localtime.split(":")[1]) >= now_localtime_set_mstart1 and int(now_localtime.split(":")[1]) < now_localtime_set_mstop1 \
                or int(now_localtime.split(":")[1]) >= now_localtime_set_mstart2 and int(now_localtime.split(":")[1]) < now_localtime_set_mstop2:
            for i in range(len(category_name)):
                if containEnglish(str(category_name[i])) != True and len(str(category_name[i])) < 5:
                    if True:

                        time.sleep(5)
                        stock = twstock.realtime.get(str(category_name[i]))

                        time.sleep(10)
                        stock1 = twstock.Stock(str(category_name[i]))
                        print("ok all ")


                        b = twstock.BestFourPoint(stock1)

                        #buy = b.best_four_point_to_buy()  # 買點分析
                        #sell = b.best_four_point_to_sell()  # 賣點分析
                        mix = b.best_four_point()  # 綜合分析 建議直接用這個 會比較快
                        mix_show = ""
                        if mix[0] == True:
                            mix_show = "做多"
                        else:
                            mix_show = "清倉"

                        average_5_days = stock1.moving_average(stock1.price, 5)[-1]
                        #average_10_days = stock1.moving_average(stock1.price, 10)[-1]
                        #average_30_days = stock1.moving_average(stock1.price, 30)[-1]

                        average_1_capacity = int((stock1.moving_average(stock1.capacity, 1)[-1]) / 1000)

                        # average_5_capacity = int((stock1.moving_average(stock1.capacity, 5)[-1]) / 1000)
                        # average_4_capacity = int((stock1.moving_average(stock1.capacity, 4)[-1]) / 1000)
########################################################################################################################
                        min = 0
                        min_idx = 0

                        for i in range(2,15):
                            if min < (get_column(i,i-1)):
                                min = get_column(i,i-1)
                                min_idx = i

########################################################################################################################
                        last_bigval_low = stock1.low[-min_idx] #停損價格

                        final_capacity = "爆大量拉" if average_1_capacity > min else "量平平"  # 是否有雙重跳空訊號

                        # if final_capacity == "爆大量拉":

                        open_stock = (stock['realtime']['open'])
                        num = stock['info']['code']
                        name = stock['info']['name']
                        low_ptr = stock['realtime']['low']
                        high_ptr = stock['realtime']['high']
                        ltr_ptr = stock['realtime']['latest_trade_price']

                        if get_two_float(ltr_ptr, 2) != "-.":
                            last_stock_val = stock1.price[-2]
                            open_stock = float(get_two_float(open_stock, 2))# 開盤價
                            now_val = float(get_two_float(ltr_ptr, 2))
                            low_val = float(get_two_float(low_ptr, 2))
                            high_val = float(get_two_float(high_ptr, 2))


                            jump_signal = True if (((now_val - last_stock_val) / now_val) * 100) > 3 else False  # 是否有跳空訊號
                            jump_strong_signal = True if low_val > average_5_days else False  # 是否有跳空五日訊號
                            final_jump = "是" if jump_signal and jump_strong_signal else "否"  # 是否有雙重跳空訊號

                            Leaderboard_num = get_two_float(num, 2)
                            Leaderboard_name = get_two_float(name, 2)



                            if final_capacity == "爆大量拉":
                                min = average_1_capacity
                                last_bigval_low = low_val

                                # # 乖離值 Y值（乖離率）＝（當日收盤價－N日內移動平均收市價）/N日內移動平均收盤價×100％
                            # bias_val = int((float(get_two_float(ltr_ptr, 2)) - average_5_days) / 5 * 100)
                            # predict_val = int(((float(get_two_float(high2330, 2)) - float(open_stock)) / (
                            #             float(get_two_float(high2330, 2)) - float(get_two_float(low2330, 2)))) * 100)

                            # \n bias_val : {"null"}%\n 成量 : {final_capacity} 綜合分析理由(買/賣) : {mix[1]} \n
                            # \n 高點價格 : {high_val}'\n 5T: {average_5_days}
                            #                                 f'\t 最低價格 : {low_val} \t 跳空訊號: {final_jump} \t開盤價 : {open_stock}
                            msg = (
                                f' \n >[參考交易，盈虧自負]< \n [股票] : {Leaderboard_num}{Leaderboard_name}\t現價 : {now_val}'
                                f'\n AI演算法綜合分析(買/賣) : {mix_show} \n AI建議停損價格 : {last_bigval_low} \t 短線停損參考 : {average_5_days}')

                            ###############################################
                            url = "https://notify-api.line.me/api/notify"
                            payload = {'message': {msg}}
                            headers = {'Authorization': 'Bearer ' + 'JBQGWjqhZkSOMv55IEhWR4P9OSHQyjNZtiOGF13Thuj'} #51fBlcQAdEIohn5XV5S9y4KJdwN0gSKGL29sNzUNQZW

                            # response = requests.request("POST", url, headers=headers, data=payload)

                            print(msg)
                            print('------------')

                    else:
                            print("ERROR")


