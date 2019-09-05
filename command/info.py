from html import escape
from telegram.ext import run_async, Filters


@run_async
def info(bot, update, gettext=False):
    if update.message:
        msg = update.message
    elif update.edited_message:
        msg = update.edited_message
    else:
        return
    text = '<code>Chat Info</code>\n' \
        f'Send Time: <code>{msg.date} +08:00</code>\n' \
        f'Message ID: <code>{msg.message_id}</code>\n' \
        f'ID: <code>{msg.chat.id}</code>\n' \
        f'Type: <code>{msg.chat.type}</code>\n'
    if msg.chat.title is not None:
        text += f'Title: <code>{escape(msg.chat.title)}</code>\n'
    if msg.chat.username is not None:
        text += f'Username: @{msg.chat.username}\n'
    if msg.chat.first_name is not None:
        text += f'First Name: <code>{escape(msg.chat.first_name)}</code>\n'
    if msg.chat.last_name is not None:
        text += f'Last Name: <code>{escape(msg.chat.last_name)}</code>\n'

    # Reply info, a `message`
    if Filters.reply(msg):
        text += '\n<code>Reply Info</code>\n' \
            f'Reply Sent Time: <code>{msg.reply_to_message.date} +08:00</code>\n' \
            f'Reply to ID: <code>{msg.reply_to_message.message_id}</code>\n' \
            f'UID: <code>{msg.reply_to_message.from_user.id}</code>\n' \
            f'Is Bot: <code>{msg.reply_to_message.from_user.is_bot}</code>\n' \
            f'First Name: <code>{msg.reply_to_message.from_user.first_name}</code>\n'
        if msg.reply_to_message.from_user.last_name is not None:
            text += f'Last Name: <code>{msg.reply_to_message.from_user.last_name}</code>\n'
        if msg.reply_to_message.from_user.username is not None:
            text += f'Username: @{msg.reply_to_message.from_user.username}\n'
        if msg.reply_to_message.from_user.language_code is not None:
            text += f'Language Code: <code>{msg.reply_to_message.from_user.language_code}</code>\n'

        # Forward info, a `message`
        if Filters.forwarded(msg.reply_to_message):
            text += '\n<code>Forward Info</code>\n'
            if msg.reply_to_message.forward_from is not None:
                # Only User Here
                text += f'User Id: <code>{msg.reply_to_message.forward_from.id}</code>\n' \
                    f'Is Bot: <code>{msg.reply_to_message.forward_from.is_bot}</code>\n' \
                    f'First Name: <code>{escape(msg.reply_to_message.forward_from.first_name)}</code>\n'
                if msg.reply_to_message.forward_from.last_name is not None:
                    text += f'Last Name: <code>{msg.reply_to_message.forward_from.last_name}</code>\n'
                if msg.reply_to_message.forward_from.username is not None:
                    text += f'Username: @{msg.reply_to_message.forward_from.username}\n'
                if msg.reply_to_message.forward_from.language_code is not None:
                    text += f'Language Code: <code>{msg.reply_to_message.forward_from.language_code}</code>\n'
            if msg.reply_to_message.forward_from_chat is not None:
                # Only Channel Here
                text += f'Channel ID: <code>{msg.reply_to_message.forward_from_chat.id}</code>\n' \
                    f'Channel Name: <code>{escape(msg.reply_to_message.forward_from_chat.title)}</code>\n'
                if msg.reply_to_message.forward_from_chat.username is not None:
                    text += f'Channel Username: @{msg.reply_to_message.forward_from_chat.username}\n'
            if msg.reply_to_message.forward_from_message_id is not None:
                text += f'Message ID: <code>{msg.reply_to_message.forward_from_message_id}</code>\n'
            if msg.reply_to_message.forward_date is not None:
                text += f'Sent Time: <code>{msg.reply_to_message.forward_date} +08:00</code>\n'
            if msg.reply_to_message.forward_signature is not None:
                text += f'Channel Sign: <code>{escape(msg.reply_to_message.forward_signature)}</code>\n'

    # Sender info, a `user`
    if not Filters.private(msg):
        text += '\n<code>Sender Info</code>\n' \
            f'UID: <code>{msg.from_user.id}</code>\n' \
            f'First Name: <code>{msg.from_user.first_name}</code>\n'
        if msg.from_user.last_name is not None:
            text += f'Last Name: <code>{msg.from_user.last_name}</code>\n'
        if msg.from_user.username is not None:
            text += f'Username: @{msg.from_user.username}\n'
        if msg.from_user.language_code is not None:
            text += f'Language Code: <code>{msg.from_user.language_code}</code>\n'
    if gettext:
        return text
    else:
        bot.send_message(chat_id=msg.chat_id,
                         text=text,
                         parse_mode='HTML')
