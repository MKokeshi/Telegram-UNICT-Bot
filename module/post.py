import telegram
import yaml
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Notice enqueueing
def enqueue_notice(context, page_data, notices_data, full_url, link_content, approval_group_chatid=None):
    logging.info("Call enqueue_notice({}, {}, {}, {}, {}, {})".format(context, page_data, notices_data, full_url, link_content, approval_group_chatid))

    channels = page_data["channels"]

    if approval_group_chatid:
        # TODO: Implement this
        # If the channel is filtered, send a request to the approval group

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Accetta ✔", callback_data = "news,approved,{},{}".format()),
                InlineKeyboardButton("Rifiuta ❌", callback_data = "news,rejected,{},{}".format())
            ]
        ])

        context.bot.sendMessage(
            chat_id = approval_group_chatid,
            text = notice_message,
            parse_mode = 'HTML',
            reply_markup = reply_markup
        )
    else:
        # Otherwise send a direct message on each channel
        
        notice_message = format_notice_message(page_data["label"], full_url, link_content)

        for channel in page_data["channels"]:
            send_notice(context, channel, notice_message)

# Message formatting
def format_content(content):
    config_map = yaml.safe_load(open("config/settings.yaml", "r"))

    max_len = config_map["max_messages_length"]

    # If message content is too long, cut it and add a footer
    if len(content) > max_len:
        split_index = max_len - 1

        while content[split_index] != ' ':
            split_index = split_index - 1

        content = "{}{}".format(content[:split_index], config_map["max_length_footer"])

    return content

def format_notice_message(label, url, link_content):
    message = "<b>[{}]</b>\n{}\n<b>{}</b>\n{}".format(
        label,
        url,
        link_content[0],
        format_content(link_content[1]),
    )

    return message

# Message send helpers
def send_notice(context, chat_id, notice_message):
    logging.info("Call send_notice({}, {}, {})".format(context, chat_id, notice_message))

    context.bot.sendMessage(
        chat_id = chat_id,
        text = notice_message,
        parse_mode = 'HTML'
    )


