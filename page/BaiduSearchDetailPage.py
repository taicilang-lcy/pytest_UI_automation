import time

from selenium.webdriver.common.by import By
from base.BasePage import BasePage
#from ..base.BasePage import BasePage
from time import sleep

#一个页面一个对象
class BaiduSearchDetailPage(BasePage):#有什么?它能干什么?#定义页面属性

    # Detail页面 对象元素定义
    # 第一个搜索结果的xpath=//*[@id="1"]/div/div[1]/h3/a

    #第2个搜索结果的xpath=//*[@id="2"]/div/h3/a/div/div/p/span/span
    #//*[@id="2"]/div/div[1]/h3/a
    # 第3个搜索结果的xpath=//*[@id="3"]/div/div[1]/h3/a
    #//*[@id="4"]/div/div[1]/h3/a
    #//*[@id="5"]/div/div[1]/h3/a
    first_res_link = (By.XPATH,'//*[@id="1"]/div/div[1]/h3/a')
    sec_res_link = (By.XPATH, '//*[@id="2"]/div/div[1]/h3/a')
    third_res_link = (By.XPATH, '//*[@id="3"]/div/div[1]/h3/a')

    #Detail页面 方法

    def search_res_Click(self):
        #time.sleep(1)
        self.click(self.first_res_link)
        self.click(self.sec_res_link)
        self.click(self.third_res_link)
        time.sleep(2)

# if __name__ == '__main__':
#     hp = BaiduSearchDetailPage()
#     hp.get_url("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=pytest&fenlei=256&rsv_pq=0xdc31802b001f8931&rsv_t=0466JhRdma%2FUpjrK4R0DSeTZbvAA%2BrZXCzFY7LQ3rzVMeOS2iMQZFe6siGwI&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=7&rsv_sug1=7&rsv_sug7=101&rsv_sug2=0&rsv_btype=i&inputT=1643&rsv_sug4=2758&rsv_sug=1")
#     hp.search_res_Click()
#     time.sleep(2)