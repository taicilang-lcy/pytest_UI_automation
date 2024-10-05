import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')  # 如果希望无头模式运行，可以取消注释

    # 初始化 Chrome WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_open_baidu(driver):
    # 打开百度
    driver.get("https://www.baidu.com")

    # 验证页面标题
    assert "百度" in driver.title

    # 验证搜索框存在
    search_box = driver.find_element(By.ID, "kw")  # 通过 ID 查找搜索框
    assert search_box is not None  # 断言搜索框不为 None

    # 进一步验证搜索框的可见性
    assert search_box.is_displayed()  # 断言搜索框是可见的
