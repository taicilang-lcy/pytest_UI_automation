from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):

        #打开浏览器和对应的驱动, 这是没有用conftest.py里定于 惰性函数的写法 conftest里有了，这里就不需要了
        # def __init__(self):
        #     #self.driver = webdriver.Chrome()
        #     self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        #     self.driver.set_window_size(1550,1000)
        #     #self.driver.set_window_position(1600,0)

        # def __init__(self,browser):
        #     self.driver = browser

        # BasePage类中的browser参数：
        # 测试用例接收到browser fixture 返回的浏览器实例（driver）后，会将其传递给BasePage类。
        # BasePage的__init__方法接收这个 browser，参数并将它赋值给 self.driver。于是self.driver就是指向了这个浏览器实例。

        def __init__(self, browser):
            self.driver = browser

        # 输入网址
        def get_url(self,url):
            self.driver.get(url)

        # send keys 键盘输入
        def send_keys(self,element,content):
            self.driver.find_element(*element).send_keys(content)

        # 点击 Click
        # def click(self,element):
        #     self.driver.find_element(*element).click()

        # 点击 Click
        def click(self, element, timeout=10):
            try:
                # 等待元素可点击
                wait = WebDriverWait(self.driver, timeout)
                clickable_element = wait.until(EC.element_to_be_clickable(element))
                clickable_element.click()
            except ElementClickInterceptedException:
                print(f"Element click intercepted for: {element}")
                # 可以添加处理逻辑，例如等待某个元素消失或关闭广告等
                self.handle_click_interception(element)
            except NoSuchElementException:
                print(f"Element not found: {element}")
            except StaleElementReferenceException:
                print(f"Stale element reference: {element}. Retrying...")
                self.click(element)  # 尝试再次点击
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        def handle_click_interception(self, element):
            # 在这里可以添加处理点击被拦截的逻辑
            print(f"Attempting to handle interception for: {element}")
            # 例如关闭弹窗、等待等

        def find_element(self, by, value, timeout=10):
            """
            查找单个元素，显式等待
            :param by: 定位方式，如 By.ID, By.XPATH
            :param value: 元素的定位值
            :param timeout: 超时时间，默认10秒
            :return: WebElement
            """
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )

        def find_elements(self, by, value, timeout=10):
            """
            查找多个元素，显式等待
            :param by: 定位方式，如 By.ID, By.XPATH
            :param value: 元素的定位值
            :param timeout: 超时时间，默认10秒
            :return: list of WebElements
            """
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )

        def get_title(self):
            """
            获取当前页面的标题
            :return: string
            """
            return self.driver.title

        def wait_for_element_to_be_visible(self, by, value, timeout=10):
            """
            等待元素可见
            :param by: 定位方式
            :param value: 元素的定位值
            :param timeout: 超时时间，默认10秒
            :return: WebElement
            """
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )

        def wait_for_page_to_load(self):
            """
            等待页面加载完成，使用 document.readyState
            """
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.execute_script("return document.readyState") == "complete"
            )

# if __name__ == '__main__':
#
#     BasePage()