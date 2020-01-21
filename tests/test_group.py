from hexlightning.functions.db_parse import group
tmp = {
    "_id": "5c2246efa6def8057c7b7bbc",
    "chat": {
        "title": "BL 原創小說群",
        "id": -1001290601308,
        "config": {
            "subscribe": [
                "🤡",
                "🔞",
                "👶",
                "😈",
                "💪",
                "👺",
                "🤖",
                "💰",
                "💩",
                "😘"
            ],
            "id": 7515,
            "admins": True,
            "ml_nsfw": True,
            "beta_filter": True
        }
    }
}


def test_group_parser():
    result = group.Group(tmp)
    assert type(result.parse()) is group.JsonObj
