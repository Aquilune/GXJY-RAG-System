# 数据源名称，使用驼峰命名法
ACTIVE_DATA_PROVIDER = 'Wind'

# 价差阈值，超出阈值给出提示
PRICE_SPREAD_THRESHOLD = 20

# 近月合约需要监测的编码
NEAR_MONTH_CODE_MONITOR = "IF2505.CFE"

# 远月合约需要监测的编码
FAR_MONTH_CODE_MONITOR = "IF2504.CFE"


DCE_URL = "https://www.founderfu.com/jiaogejicangdanguizejianbiao/426.html"
CZCE_URL = "https://www.founderfu.com/jiaogejicangdanguizejianbiao/427.html"
INE_URL = "https://www.founderfu.com/jiaogejicangdanguizejianbiao/428.html"
GFEX_URL = "https://www.founderfu.com/jiaogejicangdanguizejianbiao/477.html"

DCE_STYLE = 'width:100%;border-collapse:collapse;height:42px;'
CZCE_STYLE = 'width:100%;border-collapse:collapse;height:42px;'
INE_STYLE = 'height:42px;width:115%;border-collapse:collapse;'
GFEX_STYLE = 'width:100%;border-collapse:collapse;height:42px;'

URL_TO_EXCHANGE = {
    DCE_URL: "DCE",  # 大连商品交易所
    CZCE_URL: "CZCE",  # 郑州商品交易所
    INE_URL: "INE",  # 上海国际能源交易中心
    GFEX_URL: "GFEX"  # 广州期货交易所
}

URL_STYLE_MAPPING = {
    DCE_URL: DCE_STYLE,
    CZCE_URL: CZCE_STYLE,
    INE_URL: INE_STYLE,
    GFEX_URL: GFEX_STYLE
}