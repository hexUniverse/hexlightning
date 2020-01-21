from hexlightning.functions.db_parse import user

tmp = {
    "_id": "5c1fc9a8a6def8057c7acfe8",
    "chat": {
        "id": 525239263,
        "first_name": "$DingChen-Tsai ᕙ( 'ω' )ᕗ",
        "is_bot": False,
        "last_name": "野貓突進",
        "username": "Shawn_N",
        "language_code": "en",
        "participate": [
            -1001231231312,
            -1009582489504,
            -1008574636228,
        ]
    },
    "config": {
        "lang": "en"
    },
    "history": [
        {
            "date": 1545647589,
            "opid": 525239263,
            "until": 0,
            "reason": "太可愛",
            "tags": ["spam", "porn"]
        },
        {
            "date": 1545647608,
            "opid": 525239263,
            "until": 0,
            "reason": "太可愛",
            "tags": ["spam", "porn"]
        }
    ]
}


def test_user_parser():
    """
    > True
    """
    result = user.User(tmp)
    assert type(result.parse()) is user.UserObj
