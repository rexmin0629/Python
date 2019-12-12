"""
1.期貨(大台:TXFA0)價差比
公式 : (大台-大盤加權指數)/大盤加權指數

2.期貨(大台:TXFA0)基差
公式 : 現貨價格－期貨價格
"""

import MicroQuote
import threading
import time
from decimal import *

Str_Account = 'masterlink'
Str_Password = 'ML2856'
#   敦南機房
Str_Server_Login = '202.39.34.86:443'
Str_Server_Quote = '202.39.34.86:7777'
Str_Server_Recover = '202.39.34.86:443'
Str_Product_Info = '202.39.34.86:443'

#   交易商品代碼，如：TXFB9、TXO11000F8、2330。若為I060，則為指數代號，如：TXF。
#   若為價差商品用左斜線分隔，如：TXFD9/E9。可用符號 | 分隔取多商品，但限於同
#   一商品種類。（詳細命名規則請參考期交所網站）。若要取得股票指數，輸入TAIEX，
#   但無法與其他商品同使取報價(第二項參數為Stock)
Str_Product = 'TXFL9'
#   交易商品種類，共下列4 項：Future、Option、Stock、Warrant
Str_Product_Type = ''
#   報價資料種類，共下列4 項：I020、I030、I080、I060。證券與權值輸入空值
Str_Quote_Type = ''

Dic_Result_LogIn = {-3: '本程式已登入，請先執行登出', -1: '無法連線伺服器', 0: '資料庫異常',
                    1: '正常', 2: '密碼錯誤', 3: '無此帳號',
                    4: '無權限', 6: '聯絡客服人員', 7: '聯絡客服人員'}

Data_Prod_Target = []
Data_TAIEX = []

#   -----------------------------------------------------------------------------   Class

Threads_test = []
Thread_Stop = False
Thread_lock = threading.Lock()

class Thread_Order_RealTime(threading.Thread):
    def __init__(self, prod, prod_type, quote_type, thread_name=None):
        threading.Thread.__init__(self)
        self.prod = prod
        self.prod_type = prod_type
        self.quote_type = quote_type
        self.thread_stop = False
        self._stop_event = threading.Event()
        if thread_name is not None:
            self.name = thread_name

    def run(self):

        def target_func():
            global Data_Prod_Target
            global Data_TAIEX

            data = MicroQuote.MicroQuote_Set(self.prod, self.prod_type, self.quote_type, False)
            for i in data.quote_on_notify():
                if (self.thread_stop is True) or (i == -4):
                    break

                #print('----------------------------------------------------')
                #print("即時報價 {0}_{1}_{2} : {3}".format(self.prod, self.prod_type, self.quote_type, i))
                if self.prod_type == 'Future':
                    Data_Prod_Target = i
                elif self.prod_type == 'Stock':
                    Data_TAIEX = i
                time.sleep(0.01)

        subthread = threading.Thread(target=target_func, args=())
        subthread.setDaemon(True)   # daemon的特性：父线程退出时子线程就自动退出
        subthread.start()

        while not self.thread_stop:
            subthread.join(1)

        #print('Thread stopped')

    def stop(self):
        self.thread_stop = True
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

#   -----------------------------------------------------------------------------   Function

def SmartAPI_Login():
    return MicroQuote.MicroQuote_Login(
        Str_Account, Str_Password, Str_Server_Login, Str_Server_Quote, Str_Server_Recover, Str_Product_Info)

def Get_Input_Enter():
    global Threads_test
    global Thread_Stop

    keystrk = input('Press Enter to Exit \n')
    # thread doesn't continue until key is pressed
    #print('You pressed: ', keystrk)
    if keystrk == '':
        Thread_Stop = True
        for t in Threads_test:
            t.stop()
            print('Thread: {0} , Stop : {1}'.format(t.name, t.thread_stop))

def Get_SpreadRate():
    global Data_Prod_Target
    global Data_TAIEX

    taiex = 0.0             # 加權指數
    price_target = 0.0      # 台指
    val_spread_rate = 0.0   # 價差比
    val_Basis = 0.0         # 基差
    while Thread_Stop == False:
        print('----------------------------------------------------')
        print("即時報價 TAIEX : {0}".format(Data_TAIEX))
        print("即時報價 I020 : {0}".format(Data_Prod_Target))

        """"""
        if len(Data_TAIEX) > 0 and len(Data_Prod_Target) > 0:
            taiex = Decimal(Data_TAIEX[1])
            price_target = Decimal(Data_Prod_Target[3])
            print("加權指數 : {0} , 台指 : {1}".format(taiex, price_target))

            val_spread_rate = round(((price_target - taiex) * 100) / taiex, 3)
            val_Basis = taiex - price_target

        print("1.大台價差比 : {0} %".format(val_spread_rate))
        print("2.大台期貨基差 : {0}".format(val_Basis))
        time.sleep(1)


#   -----------------------------------------------------------------------------   Main

try:

    if __name__ == '__main__':
        result_login = SmartAPI_Login()
        print("登入: {0}".format(Dic_Result_LogIn.get(result_login, '')))

        Thread_Stop = False
        Threads_test.append(Thread_Order_RealTime(Str_Product, 'Future', 'I020', 'Thread_Future_I020'))
        Threads_test.append(Thread_Order_RealTime('TAIEX', 'Stock', '', 'Thread_Stock_TAIEX'))
        print('Future {0} Quote Start'.format(Str_Product))
        for t in Threads_test:
            t.start()

        threading.Thread(target=Get_SpreadRate).start()
        threading.Thread(target=Get_Input_Enter).start()

        for t in Threads_test:
            t.join()
            print('{0} isAlive: {1}'.format(t.name, t.isAlive()))

except Exception as ex:
    print("Error: {0}".format(ex))
