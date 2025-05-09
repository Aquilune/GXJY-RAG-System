from datetime import datetime

import pandas as pd
from pathlib import Path
from lupa import LuaRuntime
import json


def process_excel_with_lua(excel_path, lua_script_path):
    """处理Excel文件并执行Lua计算"""
    # 1. 读取Excel文件
    try:
        df = pd.read_excel(excel_path, header=None)  # 无表头读取
        log(f"成功读取Excel文件: {excel_path}")
    except Exception as e:
        raise ValueError(f"Excel文件读取失败: {str(e)}")

    # 2. 定义数据映射关系（示例配置）
    cell_mapping = {
        "LotNumber": (3, 2),  # 第3行第2列
        "Packages": (5, 4),  # 第5行第4列
        "B1": (8, 3),  # 第8行第3列
        "LAvg": (12, 5),  # 第12行第5列
        # 其他字段映射...
    }

    # 3. 提取单元格数据
    input_data = {}
    for field, (row, col) in cell_mapping.items():
        try:
            # Excel行列索引从0开始
            value = df.iloc[row - 1, col - 1]

            # 处理空值和特殊值
            if pd.isna(value):
                value = None
            elif isinstance(value, str):
                value = value.strip()

            input_data[field] = value
            log(f"提取字段 {field}: {value} (原始位置: R{row}C{col})")

        except IndexError:
            raise ValueError(f"无效的单元格位置: R{row}C{col}")

    # 4. 加载Lua脚本
    lua = LuaRuntime()
    with open(lua_script_path, 'r', encoding='utf-8') as f:
        lua_code = f.read()

    # 5. 执行Lua计算
    try:
        lua.execute(lua_code)
        lua_func = lua.globals().Count

        # 转换数据为Lua table
        lua_table = lua.table_from(input_data)

        # 执行计算
        result = lua_func(lua_table)
        log("Lua计算完成，返回结果")

        # 6. 处理返回结果
        if not result or len(result) < 33:
            raise ValueError("Lua返回结果格式不正确")

        return {
            "lot_number": str(result[1]),
            "premium": float(result[17]),
            "details": {
                "color_grades": [float(result[18]), float(result[19]), float(result[20])],
                "length_dist": [float(result[21]), float(result[22]), float(result[23])]
            },
            "is_rejected": bool(result[30]),
            "rejection_reason": str(result[31] or "")
        }

    except Exception as e:
        raise RuntimeError(f"Lua执行错误: {str(e)}")


def log(message):
    """日志记录函数"""
    print(f"[{datetime.now().isoformat()}] {message}")
