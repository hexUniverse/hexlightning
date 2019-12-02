import requests
from telegram.ext.dispatcher import run_async

from plugin import db_parse, db_tools
# from  import checker_result
# import event.xtext_filter
# from event.xtext_filter.extend_links import checker_result
# a = event.xtext_filter.extend_links.checker_result


class checker_result:
    def __init__(self):
        self.tags = list()
        self.name = str()


def get_cookie(text):
    url = 'https://getbyethostcookie.glitch.me/'
    result = requests.post(url, data={'jscode': text})
    if result.status_code == 200:
        return result.text


# @run_async
def binance(bot, update, url):
    # mongo = db_tools.use_mongo()
    r = requests.get(url)
    # if r.status_code not in [301, 302, 200]:
    #    print(r.status_code)
    #    return checker_result()
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
