import importlib
from arbitrage_app.configurations import *


# 根据配置文件中的数据供应商名称选择对应的类
def get_data_provider():
    provider_name = ACTIVE_DATA_PROVIDER
    try:
        module = importlib.import_module(f'arbitrage_app.data_providers.{provider_name}DataProvider')
        class_name = f'{provider_name}DataProvider'
        provider_class = getattr(module, class_name)
        return provider_class()
    except (ImportError, AttributeError):
        raise ValueError(f"Invalid provider: {provider_name}. Make sure the module and class exist.")
