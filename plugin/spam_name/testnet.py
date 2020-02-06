import re


class testnet:
    def __init__(self):
        self.tags = ['coin', 'scam', 'ads']

    def detect(self, full_name):
        '''
        Testnet
        return:
            tuple (True, 'QQ_Spam', [result])
        '''
        pattern = '(testnet)'
        result = re.findall(pattern, full_name)
        if result:
            return (True, 'TestNet_Spam', result)
        else:
            return (False, 'TestNet_Spam', None)
