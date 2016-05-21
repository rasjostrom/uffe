"""
Builds responses suitable for specific tasks performed by
the bot. Most of the responses here are based on the random
vocabulary defined in conversation.py in combination with
a more specific message.
"""

import conversation
import utils


def list_items(item_list):
    """Lists and formats all tasks items given by item_list along
    with a semi-randomized 'ok'-response in a single message.

    If the list is empty, a fixed error response is returned.

    :param item_list: The list of items.
    :type item_list: list of dicts.
    :returns: str -- The response message.
    """
    if len(item_list) < 1:
        return 'Sorry, it seems like there are no items to show!'
    dynamic_resp = conversation.random_ok('coma')
    static_resp = 'here is a list of your items'
    message = '{} {}:\n'.format(dynamic_resp, static_resp)

    for item in item_list:
        message += utils.format_item(**item)
    return message


def deny_taunt():
    """Returns a taunting message denying the user's request.

    :returns: str -- The response message.
    """
    return conversation.random_deny('taunt')


def create_questions():
    """Builds a dictionary of randomized questions used to
    prompt the user for proper input values when creating
    a new task item.

    :returns: dict -- A dictionary of questions.
    """
    return {
        'description': conversation.random_create('description'),
        'deadline': conversation.random_create('deadline'),
        'comments': conversation.random_create('comments'),
    }


def update_questions():
    """Builds a question regarding what about an item the
    user would like to update.

    :returns: str -- The response message.
    """
    return conversation.random_update('task')


def create_success(item):
    """Builds a 'success'-response string for when a task
    item is created.

    :param item: The created item.
    :type item: dict.
    :returns: str -- The response message.
    """
    return '{} here  is the task I created for you:\n{}'.format(
        conversation.random_ok('coma'), utils.format_item(**item))


def update_success(item):
    """Builds a 'success'-response message when a task item
    is updated.

    :param item: The updated item.
    :type item: dict.
    :returns: str -- The response message.
    """
    return '{} here  is the task I updated for you:\n{}'.format(
        conversation.random_ok('coma'), utils.format_item(**item))


def delete_confirm(item):
    """Builds a response message used when asking the user
    to confirm deletion of an item.

    :param item: The item to delete.
    :type item: dict.
    :returns: str --  The confirmation message.
    """
    return '{} delete this item?\n{}'.format(
        conversation.random_confirm('half'), utils.format_item(**item))


def delete_success():
    """Builds a 'success'-response message when a task item
    is deleted.

    :returns: str -- The response message.
    """
    return '{} it\'s gone!'.format(conversation.random_ok('coma'))


def delete_regret():
    """Builds a response message for when the user aborts the
    deletion of an item.

    :returns: str -- The response message.
    """
    return '{} then I won\'t.'.format(conversation.random_ok('coma'))


def error_retry():
    """Builds an error message for when a user request could
    not be parsed and/or acted upon.

    :returns: str -- The response message.
    """
    return conversation.random_error('retry')
