import json
import yaml
import pytest

# @pytest.fixture(scope='module')
# def json_data():
#     with open('data.json') as f:
#         return json.load(f)
#
# @pytest.fixture(scope='module')
# def yaml_data():
#     with open('data.yaml') as f:
#         return yaml.safe_load(f)

#@pytest.fixture(scope='module')
def load_yaml_data(file_path, key_field, value_fields):
    """
    从 YAML 文件加载测试数据。

    :param file_path: YAML 文件路径
    :param key_field: 键字段名称，例如 'test_cases'
    :param value_fields: 需要提取的字段名列表，例如 ['url', 'search_keyword']
    :return: 测试数据列表
    """
    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        # 提取测试数据
        test_cases = yaml_data.get(key_field, [])
        return [(tuple(case[field] for field in value_fields)) for case in test_cases]