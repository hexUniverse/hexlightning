import pyrogram
from pyrogram import Client, Message
from hexlightning.plugins import about


msg = "pyrogram.Message(message_id=1911, date=1579596337, chat=pyrogram.Chat(id=525239263, type='private', is_verified=False, is_restricted=False, is_scam=False, is_support=False, username='Shawn_N', first_name='$DingChen-Tsai (ತ◞౪◟ತ‵)', photo=pyrogram.ChatPhoto(small_file_id='AQADAQADXKgxG9-DTh8ACDTaawYABAIAA9-DTh8ABFQ1CJNb1GQrR_UBAAEWBA', big_file_id='AQADAQADXKgxG9-DTh8ACDTaawYABAMAA9-DTh8ABFQ1CJNb1GQrSfUBAAEWBA')), from_user=pyrogram.User(id=525239263, is_self=False, is_contact=False, is_mutual_contact=False, is_deleted=False, is_bot=False, is_verified=False,is_restricted=False, is_scam=False, is_support=False, first_name='$DingChen-Tsai (ತ◞౪◟ತ‵)', status='recently', username='Shawn_N', language_code='en', dc_id=1, photo=pyrogram.ChatPhoto(small_file_id='AQADAQADXKgxG9-DTh8ACDTaawYABAIAA9-DTh8ABFQ1CJNb1GQrR_UBAAEWBA', big_file_id='AQADAQADXKgxG9-DTh8ACDTaawYABAMAA9-DTh8ABFQ1CJNb1GQrSfUBAAEWBA')), mentioned=False, scheduled=False, from_scheduled=False, text='/about', entities=pyrogram.client.types.pyrogram_list.PyrogramList([pyrogram.MessageEntity(type='bot_command', offset=0, length=6)]), outgoing=False)"
msg_obj = eval(repr(msg))


def test_about():
    about.about(Client, msg_obj)
