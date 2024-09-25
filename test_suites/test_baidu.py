from page.HomePage import HomePage
from page.BaiduSearchDetailPage import BaiduSearchDetailPage
import pytest
import allure
import os
from utils.testdata_file import load_yaml_data

# 直接参数化 url和 search_keyword
# @pytest.mark.parametrize("url, search_keyword", [
#     ("https://www.baidu.com/", "automation pytest3"),    # 测试用例 1
#     ("https://www.baidu.com/", "automation pytest2"),    # 测试用例 2
#     ("https://www.baidu.com/", "automation pytest"),    # 测试用例 3
# ])


#print(os.path.join(os.path.dirname(__file__), 'test_data', 'test_data1.yaml'))
test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data', 'test_data1.yaml')


@pytest.mark.parametrize("url, search_keyword", load_yaml_data(test_data_path, 'test_cases', ['url', 'search_keyword']))
def test_baidu_01(browser, url, search_keyword):
    hp = HomePage(browser)
    # hp.get_url("https://www.baidu.com/")
    # hp.bd_search('automation pytest')
    hp.get_url(url)
    hp.bd_search(search_keyword)


def test_baidu_02(browser):
    bs = BaiduSearchDetailPage(browser)
    bs.search_res_Click()


# def test_baidu_03(browser):
#     pass

# if __name__ == '__main__':
#     pytest.main()
