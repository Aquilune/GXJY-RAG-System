import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.founderfu.com/jiaogejicangdanguizejianbiao/428.html"

# 发送请求获取网页内容
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 确保正确解码中文

# 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到目标表格 - 根据网页结构可能需要调整选择器
table = soup.find('table', {'class': 'MsoNormalTable', 'style': 'height:42px;width:115%;border-collapse:collapse;'})

if not table:
    table = soup.find('table')  # 如果class选择器不工作，尝试找第一个表格

# 提取表头
headers = []
header_cells = table.find_all(
    'td',
    style=lambda value: value and 'background:#ac0000;' in value.lower()
)

for cell in header_cells:
    # 方法1：直接提取所有文本（最简单）
    header_text = cell.get_text(strip=True)

    # 方法2：精确提取（处理特定嵌套结构）
    # 先尝试提取<b>标签内的文本
    bold_text = cell.find('b').get_text(strip=True) if cell.find('b') else ''

    # 如果没有获取到内容，尝试直接从span提取
    if not bold_text:
        span = cell.find('span', {'style': True})
        if span:
            bold_text = span.get_text(strip=True)

    # 特殊处理包含链接的情况
    link = cell.find('a')
    if link:
        link_text = link.get_text(strip=True)
        # 合并链接文本和其他文本
        bold_text = bold_text.replace(link_text, '').strip() + ' ' + link_text

    # 清理结果
    final_text = bold_text or header_text
    final_text = final_text.replace('\n', ' ').replace('\xa0', ' ').strip()

    headers.append(final_text)


# 提取数据行
data = []
for row in table.find_all('tr')[1:]:  # 跳过表头行
    row_data = []
    for td in row.find_all(['td', 'th']):
        # 处理特殊内容格式
        content = ' '.join(td.stripped_strings)  # 合并所有文本节点
        content = content.replace('\n', ' ')  # 替换换行符
        content = content.replace(' ', '')  # 删除所有空格
        row_data.append(content)

    # 确保数据行与表头列数一致
    if len(row_data) == len(headers):
        data.append(row_data)
    else:
        # 如果列数不匹配，尝试填充或截断
        if len(row_data) > len(headers):
            row_data = row_data[:len(headers)]
        else:
            row_data += [''] * (len(headers) - len(row_data))
        data.append(row_data)

# 创建DataFrame
df = pd.DataFrame(data, columns=headers)

# 保存到Excel文件
df.to_excel('上期所、能源中心期货交割规则表.xlsx', index=False)

# 打印前几行查看结果
print(df.head())