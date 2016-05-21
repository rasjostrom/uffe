import time
import datetime

from oboy import oboy
from slackclient import SlackClient
import keywords
import response
import utils

TOKEN = 'xoxb-43181503156-2iNU1mooWkkgLOCe4ejQZFTM'
bot = SlackClient(TOKEN)
BOT_ID = 'U195BET4L'


def date_context(text):
    """Pre-parsing of a user input text to try to find an
    attempt of specifying a date with normal words like
    'monday', 'last friday' or 'today'.

    If such an attempt could not be found in the text, None is
    returned instead.

    :param text: The user message text.
    :type text: str
    :returns: str -- YYYY-MM-DD format of the date or None.
    """
    for i, word in enumerate(text):
        if i < (len(text) - 1):
            if word in keywords.TIME_EXPRESSION:
                if text[i + 1] in keywords.DATE_CONTEXT:
                    return str(utils.date_from_day(word, text[i+1]))
        elif word in keywords.DATE_CONTEXT:
            return str(utils.date_from_day('this', word))
    return None


def prompt(channel, question):
    """Sends a message to a given slack channel with a given
    question, prompting for a user based input.

    After the question is sent to the channel the bot starts
    listening for a message-type slack event from a user.

    :param channel: The channel ID to prompt for input in.
    :type channel: str.
    :param question: The question to ask.
    :type question: str
    :returns: str -- The user response.
    """
    bot.rtm_send_message(channel, question)
    while True:
        data = bot.rtm_read()
        if utils.is_user_message(data, BOT_ID):
            return data[0]['text'].lower()


def process_entry(message):
    """Tries to find an entry keyword, based on the keys in
    keywords.py. If an entry key is found, control is directed
    to the proper function to further process the command
    message and respond to the right channel.

    :param message: The slack event message.
    :type message: dict
    """
    channel = message[0]['channel']
    text = message[0]['text'].lower().split()

    for word in text:
        if word in keywords.CREATE:
            return process_create(channel, text)
        elif word in keywords.READ:
            return process_read(channel, text)
        elif word in keywords.UPDATE:
            return process_update(channel, text)
        elif word in keywords.COMPLETE:
            if 'please' in text:
                return process_toggle(channel, text)
            else:
                return bot.rtm_send_message(channel, response.deny_taunt())
        elif word in keywords.DELETE:
            return process_delete(channel, text)


def process_create(channel, text):
    """Parses user input text to determine what should be
    created and prompts the user for additional details when
    required.

    Responds with a success or failure status to the channel.

    :param channel: The channel of which to respond to.
    :type channel: str.
    :param text: The user message text.
    :type text: str.
    """
    questions = response.create_questions()
    date = date_context(text)
    if date is None:
        date = date_context(prompt(channel, questions['deadline']).split())
    if date is None:
        return error_reply(channel)

    description = prompt(channel, questions['description'])
    comments = prompt(channel, questions['comments'])
    if comments in keywords.ANSWER_NEGATIVE:
        comments = ''

    item = oboy.add_item(date, description, comments, 0, False)
    message = response.create_success(item)
    bot.rtm_send_message(channel, message)


def process_read(channel, text):
    """Parses user input text to determine what should be read
    and sent back to the user.

    Responds with a success or failure status to the channel.

    :param channel: The channel  of which to respond to.
    :type channel: str.
    :param text: The user message text.
    :type text: str.
    """
    deadline = date_context(text)
    if deadline:
        item_list = oboy.list_in_range(date_from=deadline, date_to=deadline)
    else:
        dayspan = str(datetime.date.today() + datetime.timedelta(days=7))
        item_list = oboy.list_in_range(date_to=dayspan)
    message = response.list_items(item_list)
    bot.rtm_send_message(channel, message)


def process_update(channel, text):
    """Parses user input text to determine what should be
    updated and prompts the user for additional details when
    required.

    Responds with a success or failure status to the channel.

    :param channel: The channel of which to respond to.
     :type channel: str.
    :param text: The user message text.
    :type text: str.
    """
    item_id = utils.find_id(text, keywords.TASK_ITEM)
    if item_id is None:
        return error_reply(channel)

    changes = {}
    for word in text:
        if word in keywords.TASK_ITEM_PROPERTIES:
            value = prompt(channel, 'New value for {}?'.format(word))
            changes[word] = value
    if len(changes) < 1:

        field = prompt(channel, 'What field would you like to update?')
        if field in keywords.TASK_ITEM_PROPERTIES:
            value = prompt(channel, 'New value for {}?'.format(field))
            changes[field] = value
        else:
            return error_reply(channel)
    item = oboy.update_item(item_id, **changes)
    message = response.update_success(item)
    bot.rtm_send_message(channel, message)


def process_toggle(channel, text):
    """Parses user input text to determine what task item
    should be toggled between the values completed or
    incomplete.

    Responds with a success or failure status to the channel.

    :param channel: The channel of which to respond to.
    :type channel: str.
    :param text: The user message text.
    :type text: str.
    """
    item_id = utils.find_id(text, keywords.TASK_ITEM)
    if item_id is None:
        return error_reply(channel)
    item = oboy.toggle_completed(item_id)
    message = response.update_success(item)
    bot.rtm_send_message(channel, message)


def process_delete(channel, text):
    """Parses the user input text to determine what item
    should be deleted and prompts the user to confirm the
    action if an item is found.

    Responds with a success or failure status to the channel.

    :param channel: The channel of which to respond to.e
     :type channel: str.
    :param text: The user message text.
    :type text: str.
    """
    item_id = utils.find_id(text, keywords.TASK_ITEM)
    if item_id is None:
        return error_reply(channel)
    item = oboy.list_by_id(item_id)
    answer = prompt(channel, response.delete_confirm(item))
    if answer in keywords.ANSWER_POSITIVE:
        oboy.delete_item(item_id)
        bot.rtm_send_message(channel, response.delete_success())
    else:
        bot.rtm_send_message(channel, response.delete_regret())


def error_reply(channel):
    """Sends an error message to the user asking it to try
    again.

    :param channel: The channel ID of which to respond to.
    :type channel: str
    """
    bot.rtm_send_message(channel, response.error_retry())


if __name__ == "__main__":
    if bot.rtm_connect():
        while True:
            event = bot.rtm_read()
            if utils.is_user_message(event, BOT_ID):
                    process_entry(event)
            time.sleep(1)
