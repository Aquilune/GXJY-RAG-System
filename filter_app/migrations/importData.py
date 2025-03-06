import pandas as pd
import mysql.connector
from datetime import date

# 建立数据库连接
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="713001",
    database="gxjy_rag_system"
)

# 创建游标对象
myCursor = mydb.cursor()

# 读取 Excel 文件
df = pd.read_excel('20250304.xlsx')

# 处理类型不匹配的列
# 将批号列转换为字符串类型
df['批号'] = df['批号'].astype(str)

# 填充缺失值
df = df.fillna({
    '产区': '',
    '产地': '',
    '类型': '',
    '颜色级': '',
    '长度': 0,
    '强力': 0,
    '码值': 0,
    '回潮': 0,
    '含杂': 0,
    '长整': 0,
    '重量': 0,
    '仓库': '',
    '报价方式1': '',
    '结算': '',
    '运费': 0
})

# 获取当前日期
today = date.today()

# 插入数据到数据库
for index, row in df.iterrows():

    # 处理报价方式3字段
    if pd.isna(row['报价方式3']):
        quotation_method3 = None
    else:
        quotation_method3_str = str(row['报价方式3'])
        if quotation_method3_str.startswith('+'):
            quotation_method3 = float(quotation_method3_str[1:])
        elif quotation_method3_str.startswith('-'):
            quotation_method3 = -float(quotation_method3_str[1:])
        else:
            quotation_method3 = float(quotation_method3_str)

    # 处理出库基差列
    if pd.isna(row['出库基差']):
        outbound_basis = None
    else:
        # 去除 "在途" 字段
        outbound_basis_str = str(row['出库基差']).replace('在途', '')
        try:
            outbound_basis = int(outbound_basis_str)
        except (ValueError, TypeError):
            outbound_basis = None

    # 处理出价列
    if pd.isna(row['出价']):
        bid = None
    else:
        try:
            bid = int(row['出价'])
        except (ValueError, TypeError):
            bid = None

    # 处理报价方式2列
    if pd.isna(row['报价方式2']):
        quotation_method2 = None
    else:
        try:
            quotation_method2 = int(row['报价方式2'])
        except (ValueError, TypeError):
            quotation_method2 = None

    sql = """
    INSERT INTO filter_app_productdata (
        batch_number, production_area, production_place, type, color_grade,
        length, strength, code_value, moisture_regain, impurity_content,
        length_uniformity, weight, warehouse, quotation_method,
        outbound_basis, update_date, quotation_method2, quotation_method3,
        bid, settlement, freight
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row['批号'], row['产区'], row['产地'], row['类型'], row['颜色级'],
        float(row['长度']), float(row['强力']), float(row['码值']),
        float(row['回潮']), float(row['含杂']),
        float(row['长整']), float(row['重量']),
        row['仓库'], row['报价方式1'],
        outbound_basis, today, quotation_method2, quotation_method3,
        bid, row['结算'], row['运费']
    )
    try:
        myCursor.execute(sql, values)
    except mysql.connector.Error as err:
        print(f"插入第 {index + 1} 行数据时出错: {err}")

# 提交事务
mydb.commit()

# 关闭游标和数据库连接
myCursor.close()
mydb.close()