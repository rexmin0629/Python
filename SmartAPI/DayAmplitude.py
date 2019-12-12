"""
振幅
公式 : (當日最高價 - 最低價) * 100 / 參考價 %
數值單位為%，若振幅為2.5%，則回傳2.5
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

Data_Quote = ''
Val_Ref_Price = 0.0     # 參考價

#   -----------------------------------------------------------------------------   Class

Threads_test = []
Thread_Stop = False
Thread_lock = threading.Lock()

class Thread_Quote_on_OHL(threading.Thread):
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
            global Data_Quote
            global Val_Ref_Price
            val_H = 0.0         # 最高價
            val_L = 0.0         # 最低價
            val_result = 0.0    # 振幅

            for i in Data_Quote.quote_on_OHL():
                if (self.thread_stop is True) or (i == -4):
                    break
                print('----------------------------------------------------')
                print("盤中高低價 {0}_{1}_{2} : {3}".format(self.prod, self.prod_type, self.quote_type, i))
                if len(i) > 0:
                    # 振幅公式 :  (當日最高價 - 最低價) * 100 / 參考價 %
                    val_H = Decimal(i[0][2])
                    val_L = Decimal(i[0][3])
                    val_result = ((val_H - val_L) * 100) / Decimal(Val_Ref_Price)
                print("振幅: {0}".format(val_result))
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

#   -----------------------------------------------------------------------------   Main

try:

    if __name__ == '__main__':
        result_login = SmartAPI_Login()
        print("登入: {0}".format(Dic_Result_LogIn.get(result_login, '')))

        print('輸入訂閱商品 : ')
        Str_Product = input().upper()
        print('輸入訂閱商品類別  1:Future 3:Stock')
        Str_Product_Type = input()

        if Str_Product and Str_Product_Type:
            if Str_Product_Type == '1':
                Str_Product_Type = 'Future'
                Str_Quote_Type = 'I020'
            elif Str_Product_Type == '3':
                Str_Product_Type = 'Stock'
                Str_Quote_Type = ''

            Data_Quote = MicroQuote.MicroQuote_Set(Str_Product, Str_Product_Type, Str_Quote_Type, False)

            info_prod = Data_Quote.get_product(Str_Product_Type, Str_Product)
            print("商品基本資料{0}: {1}".format(Str_Product, info_prod))
            Val_Ref_Price = Decimal(info_prod[0][1])
            print("參考價 : {0}".format(Val_Ref_Price))

            Threads_test.append(Thread_Quote_on_OHL(Str_Product, Str_Product_Type, Str_Quote_Type, 'Thread_OHL'))
            threading.Thread(target=Get_Input_Enter).start()

            for t in Threads_test:
                t.start()

            for t in Threads_test:
                t.join()
                print('{0} isAlive: {1}'.format(t.name, t.isAlive()))

except Exception as ex:
    print("Error: {0}".format(ex))
