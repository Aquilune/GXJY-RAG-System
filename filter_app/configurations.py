from datetime import date

CRAWLER_LOGIN = {
    'url': 'https://www.oureway.com/users/login',
    'username': '18516175174',
    'password': '13919407312'
}

CRAWLER_PAGES = 574

CRAWLER_TARGET = "https://www.oureway.com/market/resources/xj"

today = date.today().strftime("%Y-%m-%d")
FILENAME = f"cotton-{today}.xlsx"