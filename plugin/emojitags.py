def tidy(input_):
    '''
    input emoji
    '''
    tmp = []
    for x in input_:
        if x in total:
            tmp.append(x)
    return list(set(tmp))


def to_string(input_):
    tidy_ = tidy(input_)
    result = to_list(tidy_)
    tmp, count = '', 0
    for x in result:
        count += 1
        if count == len(result):
            tmp += x
        else:
            tmp += f'{x}, '
    return tmp


def to_list(input_):
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
    if type(input_) == str and input_.isalpha() == False:
        tidy_ = to_list(tidy(input_))
    elif type(input_) == str:
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
        'coin': 0}
    for x in tidy_:
        day_list.append(day[x])
    day_list = sorted(day_list)
    if day_list[0] == 0:
        return 0
    else:
        return day_list[-1]


total = []
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

emoji_dict = {
    'halal': {
        'tw': '中東(花瓜)',
        'hint': '防止一些中東帳號，在群組內瘋狂洗版。',
        'emoji': ['🤡', '🛢', '💣', '💥', '🔪', '🔥', '🛐',
                  '✝️', '☪️', '📿', '🕌', '🕋', '🎆', '🎇', '🕉']
    },
    'porn': {
        'tw': '色情內容',
        'hint': '防止 (含有/隱含) 色情的內容',
        'emoji': ['🔞', '🚌', '🍑', '🌮', '🍆']
    },
    'child': {
        'tw': '兒童情色內容',
        'hint': '防止 (含有/隱含) 色情的內容\n⚠️兒童情色內容為違法內容，預設開啟⚠️',
        'emoji': ['👶', '🎒', '👧🏻']
    },
    'ads': {
        'tw': '廣告',
        'hint': '廣告包含帳號名稱、頭像、內容。',
        'emoji': ['😈', '👿', '💼', '📉', '💹', '📈']
    },
    'vio': {
        'tw': '暴力血腥',
        'hint': '含有血腥或暴力內容',
        'emoji': ['💪', '🤛', '🤜', '🥊']
    },
    'scam': {
        'tw': '黑產詐欺',
        'hint': '黑色產業廣告或是詐欺內容。',
        'emoji': ['👺']
    },
    'botspam': {
        'tw': '垃圾機器人',
        'hint': '大量洗版的機器人，常見為中東帳號拉入。',
        'emoji': ['🤖']
    },
    'coin': {
        'tw': '虛擬貨幣廣告',
        'hint': '發送虛擬貨幣廣告',
        'emoji': ['💰', '🐑']
    },
    'spam': {
        'tw': '垃圾訊息(全選)',
        'hint': '濫刷、無意義、垃圾訊息。',
        'emoji': ['💩', '🚮', '🚯', '🗑']
    }
}
for x in emoji_dict:
    total.extend(emoji_dict[x]['emoji'])
