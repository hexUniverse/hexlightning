
from hexlightning.functions.i18n import i18n
from pyrogram import Client, Message


def test_i18n():
    """
    > 嗨 我是 hexlightning
    """
    @i18n()
    def test_i18n_(client: Client, message: Message):
        assert _('嗨') == '嗨 我是 hexlightning'

    test_i18n_(Client, Message)
