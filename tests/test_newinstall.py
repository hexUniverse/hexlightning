import json

from hexlightning.functions.new_chat_members import new_chat_members
tmp = """{
    "caption_entities": [],
    "channel_chat_created": false,
    "chat": {
        "id": -1001425341153,
        "title": "TESTING",
        "type": "supergroup"
    },
    "date": 1561013574,
    "delete_chat_photo": false,
    "entities": [],
    "from": {
        "first_name": "@DingChen-Tsai ᕙ( "
        ω " )ᕗ",
        "id": 525239263,
        "is_bot": false,
        "language_code": "en",
        "username": "Shawn_N"
    },
    "group_chat_created": false,
    "message_id": 2903,
    "new_chat_members": [{
        "first_name": "tdc",
        "id": 12345678,
        "is_bot": true,
        "username": "tdc_bot"
    }],
    "new_chat_photo": [],
    "photo": [],
    "supergroup_chat_created": false
}"""


def test_newinstall():
    """
    > True
    """
    data = json.loads(tmp)
    new_chat_members(data)
