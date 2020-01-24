from hexlightning.functions.db_parse import user

tmp = {
    "_id": "5c1fc9a8a6def8057c7acfe8",
    "chat": {
        "id": 123456789,
        "first_name": "$DingChen-Tsai ᕙ( 'ω' )ᕗ",
        "is_bot": False,
        "last_name": "野貓突進",
        "username": "Shawn_N",
        "language_code": "en",
        "participate": [
            -100123456789,
            -100123498756
        ]
    },
    "config": {
        "lang": "en"
    },
    "history": [
        {
            "date": 1545647589,
            "opid": 612345,
            "until": 0,
            "reason": "頭像太可愛引起我犯罪慾望",
            "tags": ["spam", "ads"]
        }
    ]
}


def test_user_parser():
    result = user.User(tmp)
    u = result.parse()

    # parse correctly
    assert isinstance(u, user.UserObj)

    # mention with html escape
    assert isinstance(u.chat.mention_html, str)
