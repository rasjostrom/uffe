"""
Utility helper functions used to make things a little easier
when the bot needs to handle user interaction.
"""

import datetime


def format_item(**kwargs):
    """Formats field properties of a task item into a suitable
    string used to display the item to a user.

    :param kwargs: The item dict keys to include.
    :returns: str -- The formatted string representation.
    """
    item_str = 'Item: {}\t Status: '.format(kwargs['id'])
    if kwargs['completed']:
        item_str += 'complete\t'
    else:
        item_str += 'incomplete\t'
    item_str += 'Deadline: {}\n'.format(kwargs['deadline'])
    if len(kwargs['comments']) > 0:
        item_str += '{}\n'.format(kwargs['description'])
        item_str += '({})\n\n'.format(kwargs['comments'])
    else:
        item_str += kwargs['description'] + '\n\n'
    return str(item_str)


def date_from_day(time_expression, day):
    """Figures out the exact 'YYYY-MM-DD' date based on an
    input like 'next friday' or 'yesterday', in a time span of 3
    weeks (7 days back or 14 days ahead).

    If the day parameter is either 'yesterday', 'today' or
    'tomorrow' the time_expression will be ignored.

    If no valid date could be found, None is returned.

    :param time_expression: Past, present or future.
     :type time_expression: str.
    :param day: The day of which a date is needed.
    :type day: str.
    :returns: date object or None
    """
    if day == 'yesterday':
        return datetime.date.today() - datetime.timedelta(days=1)
    elif day == 'today':
        return datetime.date.today()
    elif day == 'tomorrow':
        return datetime.date.today() + datetime.timedelta(days=1)

    elif time_expression == 'last':
        for i in range(-7, 0):
            date = datetime.date.today() + datetime.timedelta(days=i)
            if day == date.strftime('%A').lower():
                return date

    elif time_expression == 'this':
        for i in range(0, 7):
            date = datetime.date.today() + datetime.timedelta(days=i)
            if day == date.strftime('%A').lower():
                return date

    elif time_expression == 'next':
        for i in range(7, 14):
            date = datetime.date.today() + datetime.timedelta(days=i)
            if day == date.strftime('%A').lower():
                    return date
    return None


def is_user_message(event, bot_id):
    """Checks to see if a given slack event is a user message.

    :param event: Slack event data
    :type event: dict.
    :param bot_id: The UID of the active slack bot.
    :type bot_id: str
    :returns: boolean
    """
    if len(event) > 0 and 'text' in event[0]:
        if 'user' in event[0]:
            if not event[0]['user'] == bot_id:
                return True
    return False


def find_id(text, keywords):
    for i, word in enumerate(text):
        if (i < len(text) - 1) and word in keywords:
            return int(text[i + 1])
    return None
