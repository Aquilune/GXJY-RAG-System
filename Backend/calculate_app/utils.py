import pandas as pd


def parse_certificate(file_path):
    """将Excel/CSV证书转换为Lua所需的字典格式"""
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    data = df.iloc[0].to_dict()

    # 字段映射（示例）
    return {
        'LotNumber': data.get('批号', ''),
        'B1': float(data.get('白棉1级', '0%').strip('%')) / 100,
        'LAvg': float(data.get('平均长度', '').replace('mm', '')),
        # 其他字段转换...
    }


from lupa import LuaRuntime


def execute_lua(input_data):
    lua = LuaRuntime()

    with open('calculator.lua', 'r', encoding='utf-8') as f:
        lua_code = f.read()

    lua.execute(lua_code)
    lua_func = lua.globals().Count
    lua_table = lua.table_from(input_data)

    result = lua_func(lua_table)  # 调用Lua主函数

    # 将Lua数组结果转换为字典
    return {
        'premium': result[16],  # 根据实际输出位置调整
        'details': {
            'color_grades': result[17:20],
            'length_dist': result[20:25]
        }
    }