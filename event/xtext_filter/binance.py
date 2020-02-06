import requests


class checker_result:
    def __init__(self):
        self.tags = list()
        self.name = str()


def get_cookie(text):
    url = 'https://getbyethostcookie.glitch.me/'
    result = requests.post(url, data={'jscode': text})
    if result.status_code == 200:
        return result.text


def binance(bot, update, url):
    r = requests.get(url)
    get_ = get_cookie(r.text)
    if get_:
        cookies = get_.split('=')
    else:
        return checker_result()
    if len(cookies) < 2:
        return checker_result()
    else:
        cookies = cookies[1]

    r = requests.get(url, cookies={"__test": cookies})
    if '<a href="https://www.binance.com/">Binance</a>' in r.text:
        result = checker_result()
        result.name = __name__
        result.tags = ['coin', 'ads']
        return result
