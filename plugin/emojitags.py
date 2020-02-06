'''emoji_dict = {
            'halal': ['🤡', '🛢', '💣', '💥', '🔪', '🔥', '🛐',
                    '✝️', '☪️', '📿', '🕌', '🕋', '🎆', '🎇', '🕉'],
            'porn': ['🔞', '🚌', '🍑', '🌮', '🍆'],
            'child': ['👶', '🎒', '👧🏻'],
            'spam': ['💩', '🚮', '🚯', '🗑'],
            'ads': ['😈', '👿', '💼', '📉', '💹', '📈'],
            'vio': ['💪', '🤛', '🤜', '🥊'],
            'scam': ['👺'],
            'botspam': ['🤖'],
            'coin': ['💰', '🐑']
        }'''
import gettext
_ = gettext.gettext


class emojitags:
    def __init__(self):
        self.total = []
        self.emoji_dict = None
        self.halal = None
        self.porn = None
        self.child = None
        self.spam = None
        self.ads = None
        self.vio = None
        self.scam = None
        self.botspam = None
        self.coin = None
        self.harass = None

        self.loads()

    def loads(self):
        self.emoji_dict = {
            'halal': {
                'title': _('中東(花瓜)'),
                'hint': _('防止中東帳號在群組內洗版。'),
                'emoji': ['🤡', '🛢', '💣', '💥', '🔪', '🔥', '🛐',
                          '✝️', '☪️', '📿', '🕌', '🕋', '🎆', '🎇', '🕉']
            },
            'porn': {
                'title': _('色情內容'),
                'hint': _('防止 (含有/隱含) 色情的內容'),
                'emoji': ['🔞', '🚌', '🍑', '🌮', '🍆']
            },
            'child': {
                'title': _('兒童情色內容'),
                'hint': _('防止 (含有/隱含) 色情的內容\n⚠️兒童情色內容為違法內容，預設開啟⚠️'),
                'emoji': ['👶', '🎒', '👧🏻']
            },
            'ads': {
                'title': _('廣告'),
                'hint': _('廣告包含帳號名稱、頭像、內容。'),
                'emoji': ['😈', '👿', '💼', '📉', '💹', '📈']
            },
            'vio': {
                'title': _('暴力血腥'),
                'hint': _('含有血腥或暴力內容'),
                'emoji': ['💪', '🤛', '🤜', '🥊']
            },
            'scam': {
                'title': _('黑產詐欺'),
                'hint': _('黑色產業廣告或是詐欺內容。'),
                'emoji': ['👺']
            },
            'botspam': {
                'title': _('垃圾機器人'),
                'hint': _('大量洗版的機器人，常見為中東帳號拉入。'),
                'emoji': ['🤖']
            },
            'coin': {
                'title': _('虛擬貨幣廣告'),
                'hint': _('發送虛擬貨幣廣告'),
                'emoji': ['💰', '🐑']
            },
            'harass': {
                'title': _('私訊騷擾'),
                'hint': _('私訊騷擾群組內成員'),
                'emoji': ['😘']
            },
            'spam': {
                'title': _('全選(所有垃圾訊息)'),
                'hint': _('濫刷、無意義、垃圾訊息。'),
                'emoji': ['💩', '🚮', '🚯', '🗑']
            }

        }

        for x in self.emoji_dict:
            self.total.extend(self.emoji_dict[x]['emoji'])

        class halal:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['halal']['emoji']
                self.hint = emoji_dict['halal']['hint']
                self.title = emoji_dict['halal']['title']

        class porn:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['porn']['emoji']
                self.hint = emoji_dict['porn']['hint']
                self.title = emoji_dict['porn']['title']

        class child:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['child']['emoji']
                self.hint = emoji_dict['child']['hint']
                self.title = emoji_dict['child']['title']

        class spam:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['spam']['emoji']
                self.hint = emoji_dict['spam']['hint']
                self.title = emoji_dict['spam']['title']

        class ads:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['ads']['emoji']
                self.hint = emoji_dict['ads']['hint']
                self.title = emoji_dict['ads']['title']

        class vio:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['vio']['emoji']
                self.hint = emoji_dict['vio']['hint']
                self.title = emoji_dict['vio']['title']

        class scam:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['scam']['emoji']
                self.hint = emoji_dict['scam']['hint']
                self.title = emoji_dict['scam']['title']

        class botspam:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['botspam']['emoji']
                self.hint = emoji_dict['botspam']['hint']
                self.title = emoji_dict['botspam']['title']

        class coin:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['coin']['emoji']
                self.hint = emoji_dict['coin']['hint']
                self.title = emoji_dict['coin']['title']

        class harass:
            def __init__(self, emoji_dict):
                self.emoji = emoji_dict['coin']['emoji']
                self.hint = emoji_dict['coin']['hint']
                self.title = emoji_dict['coin']['title']

        self.halal = halal(self.emoji_dict)
        self.porn = porn(self.emoji_dict)
        self.child = child(self.emoji_dict)
        self.spam = spam(self.emoji_dict)
        self.ads = ads(self.emoji_dict)
        self.vio = vio(self.emoji_dict)
        self.scam = scam(self.emoji_dict)
        self.botspam = botspam(self.emoji_dict)
        self.coin = coin(self.emoji_dict)
        self.harass = harass(self.emoji_dict)


total = emojitags().total
emoji_dict = emojitags().emoji_dict


def tidy(input_):
    '''
    input emoji
    string to list
    '''
    tmp = []
    for x in input_:
        if x in total:
            tmp.append(x)
    return list(set(tmp))


def to_string(input_):
    # to a list like string
    tidy_ = tidy(input_)
    result = to_list(tidy_)
    return ', '.join(result)


def to_list(input_):
    '''
    to list
    '''
    tidy_ = tidy(input_)
    tmp = []

    for detect in tidy_:
        for whole in emoji_dict:
            emoji_type = emoji_dict[whole]['emoji']
            if detect in emoji_type and whole not in tmp:
                tmp.append(whole)
    return tmp


def to_emoji(input_):
    '''
    input [list]
    '''
    tmp = ''
    for x in input_:
        if x not in emoji_dict.keys():
            return
        tmp += emoji_dict[x]['emoji'][0]
    return ''.join(e for e in list(set(tmp)))


def druation(input_):
    '''
    input list
    '''
    day_list = []
    if isinstance(input_, str) and input_.isalpha() == False:
        tidy_ = to_list(tidy(input_))
    elif isinstance(input_, str):
        return 'not a list.'
    else:
        tidy_ = input_
    day = {
        'halal': 0,
        'porn': 30,
        'child': 0,
        'spam': 7,
        'ads': 0,
        'vio': 14,
        'scam': 0,
        'botspam': 0,
        'coin': 0,
        'harass': 7}
    for x in tidy_:
        day_list.append(day[x])
    day_list = sorted(day_list)
    if day_list[0] == 0:
        return 0
    else:
        return day_list[-1]
