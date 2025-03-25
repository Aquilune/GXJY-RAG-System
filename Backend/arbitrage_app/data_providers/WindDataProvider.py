from arbitrage_app.data_providers.BaseDataProvider import BaseDataProvider

# 当前数据提供商为万得
from WindPy import w

w.start()
w.isconnected()


# w.menu()
# print(w.wsq("IF2504.CFE","rt_settle,rt_est_settle"))
# user_input = input("请输入任意内容，然后按回车键继续：")

class WindDataProvider(BaseDataProvider):
    def get_near_month_price(self, near_code):
        if w.isconnected():
            return w.wsq(near_code, "rt_latest").Data[0][0]
        else:
            return "Wind is not connected"

    def get_far_month_price(self, far_code):
        if w.isconnected():
            return w.wsq(far_code, "rt_latest").Data[0][0]
        else:
            return "Wind is not connected"
