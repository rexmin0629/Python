import haohaninfo
import pandas as pd
import numpy as np
import inline
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mpl_finance as mpf
import talib
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

"""
券商代碼，如：Yuanta（元大證券）、Capital（群益證券）、Capital_Future（群益期貨）、Kgi（凱基證券）、
Kgi_Future（凱基期貨）、Simulator（虛擬期貨）、Masterlink_Future（元富期貨）、Concord_Future（康和期貨）。
"""
Dic_BrokerID = {1: 'Yuanta', 2: 'Capital', 3: 'Capital_Future',
                4: 'Kgi', 5: 'Kgi_Future', 6: 'Simulator',
                7: 'Masterlink_Future', 8: 'Concord_Future'}

#   -----------------------------------------------------------------------------   Function

class Application(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.label = tk.Label(self)
        self.label["text"] = "Stock :"
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=0, pady=10)

        self.button = tk.Button(self)
        self.button["text"] = "Show KBar"
        self.button.grid(row=1, column=1, padx=0, pady=0)


#   -----------------------------------------------------------------------------   Main

try:

    if __name__ == '__main__':

        """
        window = tk.Tk()
        window.title('GOrder Sample')
        window.geometry('250x100')
        window.resizable(False, False)
        Application(window)
        window.mainloop()"""


        #   券商代碼
        str_BrokerID = Dic_BrokerID.get(7)
        #   交易商品代碼，如：2330、TXFF9，若要取多商品報價以逗號分隔
        str_Product = 'TXFK9'
        #   報價種類，如：match（成交資訊）、commission（委託資訊）、updn5（上下五檔資訊）。
        str_Table = 'updn5'

        GO = haohaninfo.GOrder.GOQuote()
        GC = haohaninfo.GOrder.GOCommand()

        #   訂閱商品
        """
        GC.AddQuote(str_BrokerID, str_Product)"""

        #   取逐筆即時報價
        """
        for i in GO.Describe(str_BrokerID, str_Table, str_Product):
            print(i)"""

        #   取最近一筆即時報價
        """
        print(GO.DescribeLast(str_BrokerID, str_Table, str_Product))"""

        #   中斷即時報價迴圈
        """
        for i in GO.Describe(str_BrokerID, str_Table, str_Product):
            print(i)
            GO.EndDescribe()"""

        #   取帳務紀錄
        """ 參數:  券商代碼，委託書號，如：05220001、05220002、0AdEZ、All。
        for i in GC.GetAccount(str_BrokerID, 'All'):
            print(i)"""

        #   取成交紀錄
        """ 參數:  券商代碼，委託書號，如：05220001、05220002、0AdEZ、All。
        for i in GC.MatchAccount(str_BrokerID, 'All'):
            print(i)"""

        #   取庫存紀錄
        """
        for i in GC.GetInStock(str_BrokerID):
            print(i)"""

        #   取歷史日K棒
        """ 
        參數:  
        K棒數量     -取最近N根的日K棒，不含當日，如：5、10、20 (最多僅能取近五年)
        商品代碼    -如：2330（股票）、006205（權證）、TXF（期貨近月）、TXFH9（期貨指定月份）、TXO（選擇權全部履約價近月買賣權）、TXO10300（選擇權指定履約價近月買賣權）、TXO10300H9（選擇權指定履約價指定月份買權）
        商品種類    -如：Stock（股票）、Warrant（權證）、Future（期貨）、Option（選擇權）
        日夜盤      -如：0（全盤）、1（日盤）、2（夜盤）
        """
        KBar = haohaninfo.GOrder.GetHistoryKBar('60', '2330', 'Stock', '0')
        #for i in KBar:
        #    print(i)

        df = pd.DataFrame(
            columns=['Date', 'Prod', 'Open', 'High', 'Low', 'Close', 'Deal_Val'],
            data=[row.split(',') for row in KBar[0:]])
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df.set_index('Date', inplace=True)
        #print(df)


        """
        df['Close'].plot(color='red')
        plt.title('2330')
        plt.grid(True)"""

        arr_f_Open = np.array(df['Open']).astype(float)
        arr_f_High = np.array(df['High']).astype(float)
        arr_f_Low = np.array(df['Low']).astype(float)
        arr_f_Close = np.array(df['Close']).astype(float)
        arr_f_Deal_Val = np.array(df['Deal_Val']).astype(float)

        sma_20 = talib.SMA(arr_f_Close, 10)

        K, D = talib.STOCH(high = arr_f_High,
                           low = arr_f_Low,
                           close = arr_f_Close,
                           fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

        fig = plt.figure(figsize=(8, 6))
        """ fig.add_axes([left, bottom, width, height])
        ax = fig.add_axes([0.1, 0.35, 0.85, 0.6])
        ax2 = fig.add_axes([0.1, 0.05, 0.85, 0.2])"""
        gs = gridspec.GridSpec(3, 1)
        ax = plt.subplot(gs[0, 0])
        ax2 = plt.subplot(gs[1, 0])
        ax3 = plt.subplot(gs[2, 0])

        ax.set_xticks(range(0, len(df.index), 10))
        ax.set_xticklabels(df.index[::10])
        mpf.candlestick2_ochl(ax, arr_f_Open, arr_f_Close, arr_f_High, arr_f_Low,
                              width=0.6, colorup='r', colordown='g', alpha=0.75)
        ax.plot(sma_20, label= str(len(KBar)) + 'days Avg')

        mpf.volume_overlay(ax2, arr_f_Open, arr_f_Close, arr_f_Deal_Val,
                           colorup='r', colordown='g', width=0.5, alpha=0.75)
        ax2.set_xticks(range(0, len(df.index), 10))
        ax2.set_xticklabels(df.index[::10])

        ax3.plot(K, label='K value')
        ax3.plot(D, label='D value')
        ax3.set_xticks(range(0, len(df.index), 10))
        ax3.set_xticklabels(df.index[::10])

        ax.legend(loc='upper left')
        ax3.legend(loc='upper left')
        plt.show()

except Exception as ex:
    print("Error: {0}".format(ex))
