import MicroQuote
import threading
import time

Str_Account = 'masterlink'
Str_Password = 'ML2856'
Str_Server_Login = '202.39.34.86:443'
Str_Server_Quote = '202.39.34.86:7777'
Str_Server_Recover = '202.39.34.86:443'
Str_Product_Info = '202.39.34.86:443'

#   交易商品代碼，如：TXFB9、TXO11000F8、2330。若為I060，則為指數代號，如：TXF。
#   若為價差商品用左斜線分隔，如：TXFD9/E9。可用符號 | 分隔取多商品，但限於同
#   一商品種類。（詳細命名規則請參考期交所網站）。若要取得股票指數，輸入TAIEX，
#   但無法與其他商品同使取報價(第二項參數為Stock)
Str_Product = ''
#   交易商品種類，共下列4 項：Future、Option、Stock、Warrant
Str_Product_Type = ''
#   報價資料種類，共下列4 項：I020、I030、I080、I060。證券與權值輸入空值
Str_Quote_Type = ''

Dic_Result_LogIn = {-3: '本程式已登入，請先執行登出', -1: '無法連線伺服器', 0: '資料庫異常',
                    1: '正常', 2: '密碼錯誤', 3: '無此帳號',
                    4: '無權限', 6: '聯絡客服人員', 7: '聯絡客服人員'}

#   -----------------------------------------------------------------------------   Class

Threads_test = []

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
        """
                data = MicroQuote.MicroQuote_Set(self.prod, self.prod_type, self.quote_type, False)

                for i in data.quote_on_notify():
                    if (self.thread_stop is True) or (i == -4):
                        break
                    print('----------------------------------------------------')
                    print("即時報價 {0}_{1}_{2} : {3}".format(self.prod, self.prod_type, self.quote_type, i))
                    time.sleep(0.01)"""

        def target_func():
            data = MicroQuote.MicroQuote_Set(self.prod, self.prod_type, self.quote_type, False)
            for i in data.quote_on_notify():
                if (self.thread_stop is True) or (i == -4):
                    break
                print('----------------------------------------------------')
                print("即時報價 {0}_{1}_{2} : {3}".format(self.prod, self.prod_type, self.quote_type, i))
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
    global Str_Account, Str_Password, Str_Server_Login, Str_Server_Quote, Str_Server_Recover, Str_Product_Info
    return MicroQuote.MicroQuote_Login(
        Str_Account, Str_Password, Str_Server_Login, Str_Server_Quote, Str_Server_Recover, Str_Product_Info)

def Set_Quote():
    global Str_Product, Str_Product_Type

    print('輸入訂閱商品 : ')
    Str_Product = input().upper()
    print('輸入訂閱商品類別  1:Future 2:Option 3:Stock 4:Warrant')
    Str_Product_Type = input()

    if Str_Product and Str_Product_Type:
        if Str_Product == 'TAIEX':
            Str_Product_Type = '3'

        s_order = {'0': Other, '1': Future, '2': Option, '3': Stock, '4': Warrant}
        s_order.get(Str_Product_Type, '0')(Str_Product)

def Get_Input_Enter():
    global Threads_test
    keystrk = input('Press Enter to Exit \n')
    # thread doesn't continue until key is pressed
    #print('You pressed: ', keystrk)
    if keystrk == '':
        for t in Threads_test:
            t.stop()
            print('Thread: {0} , Stop : {1}'.format(t.name, t.thread_stop))

def Future(prod):
    global Threads_test
    Threads_test = []
    Threads_test.append(Thread_Order_RealTime(prod, 'Future', 'I020', 'Thread_Future_I020'))
    Threads_test.append(Thread_Order_RealTime(prod, 'Future', 'I030', 'Thread_Future_I030'))
    Threads_test.append(Thread_Order_RealTime(prod, 'Future', 'I080', 'Thread_Future_I080'))
    threading.Thread(target=Get_Input_Enter).start()

    print('Future {0} Quote Start'.format(prod))
    for t in Threads_test:
        t.start()

    for t in Threads_test:
        t.join()
        print('{0} isAlive: {1}'.format(t.name, t.isAlive()))
    print('Future {0} Quote End'.format(prod))
    Set_Quote()

def Option(prod):
    global Threads_test
    Threads_test = []
    Threads_test.append(Thread_Order_RealTime(prod, 'Option', 'I020', 'Thread_Option_I020'))
    Threads_test.append(Thread_Order_RealTime(prod, 'Option', 'I030', 'Thread_Option_I030'))
    Threads_test.append(Thread_Order_RealTime(prod, 'Option', 'I080', 'Thread_Option_I080'))
    threading.Thread(target=Get_Input_Enter).start()

    print('Option {0} Quote Start'.format(prod))
    for t in Threads_test:
        t.start()

    for t in Threads_test:
        t.join()
        print('{0} isAlive: {1}'.format(t.name, t.isAlive()))
    print('Option {0} Quote End'.format(prod))
    Set_Quote()

def Stock(prod):
    global Threads_test
    Threads_test = []
    Threads_test.append(Thread_Order_RealTime(prod, 'Stock', '', 'Thread_Stock'))
    threading.Thread(target=Get_Input_Enter).start()

    print('Stock {0} Quote Start'.format(prod))
    for t in Threads_test:
        t.start()

    for t in Threads_test:
        t.join()
        print('{0} isAlive: {1}'.format(t.name, t.isAlive()))
    print('Stock {0} Quote End'.format(prod))
    Set_Quote()

def Warrant(prod):
    global Threads_test
    Threads_test = []
    Threads_test.append(Thread_Order_RealTime(prod, 'Warrant', '', 'Thread_Warrant'))
    threading.Thread(target=Get_Input_Enter).start()

    print('Warrant {0} Quote Start'.format(prod))
    for t in Threads_test:
        t.start()

    for t in Threads_test:
        t.join()
        print('{0} isAlive: {1}'.format(t.name, t.isAlive()))
    print('Warrant {0} Quote End'.format(prod))
    Set_Quote()

def Other(prod):
    print('Other {0}'.format(prod))

#   -----------------------------------------------------------------------------   Main

try:

    if __name__ == '__main__':

        result_login = SmartAPI_Login()
        print("登入: {0}".format(Dic_Result_LogIn.get(result_login, '')))

        Set_Quote()

        #   訂閱商品
        """
        data = MicroQuote.MicroQuote_Set(Str_Product, Str_Product_Type, Str_Quote_Type, False)
        for i in data.quote_on_notify():
            print("及時報價 {0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, i))"""

        #   取得一筆當前報價。可用符號 | 分隔取多商品。
        """
        data_Last = data.get_last_data(Str_Product_Type, Str_Product, Str_Quote_Type)
        print("{0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, data_Last))"""

        #   可輸入起始以及 結束時間進行資料回補
        """
        for i in data.get_history_data('09:00:00', '10:00:00'):
            print("歷史資料回補 {0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, i))"""

        #   訂閱交易商品後，進行資料回補並取得逐筆報價。True為回補最後一筆、 False為全回補，預設為 False
        """
        for i in data.recover_on_notify(False):
            print("回補並報價 {0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, i))"""

        #   訂閱交易商品後，可取得該日商品列表
        """
        list_prod = data.get_list()
        print("該日商品列表數量{0}: {1}".format(Str_Product_Type, len(list_prod)))
        print("該日商品列表{0}: {1}".format(Str_Product_Type, list_prod))"""

        #   取得該日商品基本資料。可用逗號(,)分隔取多商品。
        """
        info_prod = data.get_product(Str_Product_Type, Str_Product)
        print("商品基本資料{0}: {1}".format(Str_Product, info_prod))"""

        #   取得該日商品盤後靜態資料。可用逗號(,)分隔取多商品。
        """
        data_Aft = data.get_after_hour(Str_Product_Type, Str_Product)
        print("商品盤後靜態資料{0}: {1}".format(Str_Product, data_Aft))"""

        #   取得盤中高低價。可用逗號(,)分隔取多商品。
        """
        data_OHL = data.get_OHL(Str_Product_Type, Str_Product)
        print("商品盤中高低價{0}: {1}".format(Str_Product, data_OHL))"""

        #   回傳伺服器時間
        """
        for i in data.heart_beat_server_time():
            print("伺服器時間 : {0}".format(i))"""

        #   訂閱股票指數，可搭配迴圈取得逐筆報價
        """
        for i in data.queue_on_taiex():
            print("指數 {0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, i))"""

        #   訂閱盤中高低價 ，可搭配迴圈取得逐筆報價
        """
        for i in data.quote_on_OHL():
            print("盤中高低價 {0}_{1}_{2} : {3}".format(Str_Product, Str_Product_Type, Str_Quote_Type, i))"""

        #   取得帳務權限狀態
        """
        val_User_Permission = data.user_permission
        print("取得帳務權限狀態: {0}".format(val_User_Permission))"""

except Exception as ex:
    print("Error: {0}".format(ex))
