import allure
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.db_manager import DatabaseManager  # 从 utils 文件夹导入
#from Automation_UI.utils.testdata_file import json_data, yaml_data  # 从 utils 文件夹导入测试数据文件处理函数
import os
import json  # 导入 json 模块
import yaml  # 导入 yaml 模块

# Define driver
driver = None

# 配置日志
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)  # 设置全局日志级别为 WARNING，忽略 INFO 和 DEBUG 级别的日志
logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def browser():
    global driver
    #"""在整个测试会话中只打开一次浏览器"""
    if driver is None:
        # for CICD container automation running
        chrome_options = Options()
        chrome_options.add_argument('window-size=1920x1080')  # 设置浏览器窗口大小
        #chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
        chrome_options.add_argument("--no-sandbox")  #  取消沙盒模式
        chrome_options.add_argument('--headless') # 无头模式
        chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 使用
        #chrome_options.add_argument('--remote-debugging-pipe')
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")  # 增加日志级别
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        logger.info("Starting test session setup, Chrome has been launched!")

        print(driver.capabilities)  # 输出浏览器的能力信息，包括版本

        # 获取浏览器和 WebDriver 版本信息
        browser_version = driver.capabilities['browserVersion']
        driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]

        # 打印版本信息到日志
        logger.info(f"Browser Version: {browser_version}")
        logger.info(f"ChromeDriver Version: {driver_version}")

        # driver.set_window_size(1550, 1000)
        # driver.set_window_position(1600,0)
        # 获取屏幕的宽度和高度       设置窗口大小和位置，分屏到右半边
        # screen_width = driver.execute_script("return window.screen.width")
        # screen_height = driver.execute_script("return window.screen.height")
        # driver.set_window_size(screen_width // 2, screen_height)
        # driver.set_window_position(screen_width // 2, 0)

        logger.info("Starting test session setup, Chrome has been launched!")
        # driver.maximize_window()

        # 设置隐式等待时间为10秒
        driver.implicitly_wait(10)

    yield driver #在Pytest测试用例中，如果有测试用例使用了browser fixture，Pytest会先执行conftest.py中的 browser fixture，创建浏览器实例并通过 yield driver 返回这个实例

    # BasePage类中的browser参数：
    # 测试用例接收到browser fixture 返回的浏览器实例（driver）后，会将其传递给BasePage类。
    # BasePage的__init__方法接收这个 browser，参数并将它赋值给 self.driver。于是self.driver就是指向了这个浏览器实例。

    # 测试会话结束时关闭浏览器
    driver.quit()
    logger.info("test session ended, teardown")


# src/my_project/tests/conftest.py

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #后置处理
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        # 实现失败截图和添加allure附件
        img = driver.get_screenshot_as_png()
        # 把图片放到allure测试报告里
        allure.attach(img,'failed screenshot', allure.attachment_type.PNG)


@pytest.fixture(scope='session')
def db():
    # 初始化数据库连接
    db_manager = DatabaseManager()
    # 创建测试表
    db_manager.execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")

    yield db_manager  # 提供数据库管理实例给测试用例使用

    # 测试结束时清理数据库
    db_manager.execute_query("DROP TABLE IF EXISTS users")
    db_manager.close_connection()

@pytest.fixture(scope='module')
def json_data():
    # 使用相对路径指定 JSON 数据文件的位置
    file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'test_data2.json')
    print(file_path)
    #file_path = r'test_data\test_data2.json'
    with open(file_path) as f:
        return json.load(f)

# 定义 YAML 数据夹具
@pytest.fixture(scope='module')
def yaml_data():
    # 使用相对路径指定 YAML 数据文件的位置
    file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'test_data1.yaml')
    print(file_path)
    #file_path = r'test_data\test_data1.yaml'
    with open(file_path) as f:
        return yaml.safe_load(f)