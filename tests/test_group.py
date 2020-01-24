from hexlightning.functions.db_parse import group
tmp = {
    "_id": "5c2246efa6def8057c7b7bbc",
    "chat": {
        "title": "小唯好嚴格 Q_Q",
        "id": -100123456789,
        "config": {
            "subscribe": ["spam", "ads"],
            "id": 7515,
            "admins": True,
            "ml_nsfw": True,
            "beta_filter": True
        }
    }
}


def test_group_parser():
    """
    > True
    """
    result = group.Group(tmp)
    assert type(result.parse()) is group.JsonObj
