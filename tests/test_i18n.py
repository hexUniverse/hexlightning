
from hexlightning.functions.i18n import i18n
from pyrogram import Client, Message


def test_i18n():

    @i18n()
    def test_i18n_(client: Client, message: Message):
        """
        > I'm hexlightning
        """
        print(_('我是海克斯'))

    test_i18n_(Client, Message)
