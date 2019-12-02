import re
import requests


def error(bot, update, error):
    full_text = str(error.__context__.object)
    pattern = '(\"update_id\":(\d+),)'
    result = re.findall(pattern, full_text)
    url = f'https://api.telegram.org/bot{bot.token}/getUpdates'
    data = {'offset': str(int(result[1][1])+1), 'limit': '1'}
    tmp = requests.post(url, data=data)
