"""
 A small response-vocabulary with functions for
randomizing a simple phrase related to how the bot should
respond. This gives the bot a little warmer feel to the user.

These functions and lists should never be accessed directly
by the bot however, but through properly built responses
defined in responses.py.
"""

import random


RESP_OK = {
    'fullstop': [
        'You got it!', 'Alright.', 'Yes, Sir!', 'Okay.', 'Sure.', 'No problem!',
    ],
    'coma': [
        'Alright,', 'Okay,', 'Sure,', 'Got it,',
    ],
}

RESP_DENY = {
    'taunt': [
        'Ah-ah-aah! You didn\'t say the magic word!',
        'Maybe if you ask nicely... :)',
    ],
}

RESP_ERROR = {
    'retry':  [
        'Sorry, I didn\'t get that, let\'s try again.',
    ],
    'exit': [
        'Sorry I\'m not sure what you mean.', 'I don\'t know what that is.',
    ],
}

QUESTION_CREATE = {
    'description': [
        'What is the task?', 'How would you describe this task?',
        'Whats the description?',
    ],
    'deadline': [
        'When should this be completed?', 'When must this be done?',
        'What\'s the deadline for this task?',
    ],
    'importance': [
        'How important is this?', 'What is the importance of this task?',
    ],
    'comments': [
        'Any comments on this task?',
        'Would you like to add any comments to this?',
    ],
}

QUESTION_UPDATE = {
    'task': [
        'What field would you like to update?', 'What are we changing?',
        'What would you like me to change about it?',
    ]
}

CONFIRM = {
    'half': [
        'Are you really sure that you want to', 'Really', 'Do you want to',
    ],
}


def random_ok(style):
    return random.choice(RESP_OK[style])


def random_deny(style):
    return random.choice(RESP_DENY[style])


def random_create(style):
    return random.choice(QUESTION_CREATE[style])


def random_update(style):
    return random.choice(QUESTION_UPDATE[style])


def random_error(style):
    return random.choice(RESP_ERROR[style])


def random_confirm(style):
    return random.choice(CONFIRM[style])
