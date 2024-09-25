from selenium.webdriver.common.by import By
from base.BasePage import BasePage
#from ..base.BasePage import BasePage
from time import sleep

#一个页面一个对象
class HomePage(BasePage):#有什么?它能干什么?#定义页面属性

    # 定义页面里的对象xpath
    # 传入参数 带有小括号 就是元组，多个参数，就要加个* 进行解包，把(By.XPATH,'//*[@id="kw"]')里面当作2个参数用
    bd_keyword =(By.XPATH,'//*[@id="kw"]')
    # 点击搜索
    bd_search_button=(By.XPATH,'//*[@id="su"]')

    # 定义这个页面里的功能，封装为函数
    def bd_search(self,keyword):
        self.send_keys(self.bd_keyword,keyword)
        self.click(self.bd_search_button)
     #   sleep(5)

# if __name__ == '__main__':
#     hp = HomePage()
#     hp.get_url("https://www.baidu.com/")
#     hp.bd_search('ddd')