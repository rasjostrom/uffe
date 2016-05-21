"""
Keywords used to parse a users input and decide how to
react to it.
"""

CREATE = [
    'add', 'create',
]

READ = [
    'list', 'display', 'show', 'get',
]

UPDATE = [
    'update', 'change',
]

COMPLETE = [
    'toggle', 'complete', 'finished',
]

TASK_ITEM = [
    'task', 'item',
]

TASK_ITEM_PROPERTIES = [
    'description', 'comment', 'deadline', 'weight',
]

DELETE = [
    'delete', 'remove',
]

TIME_EXPRESSION = [
    'this', 'next', 'last',
]

DATE_CONTEXT = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday', 'today', 'tomorrow', 'yesterday',
]


ANSWER_NEGATIVE = [
        'no', 'nope', 'nah', 'negative',
]

ANSWER_POSITIVE = [
        'yes', 'yep', 'yeah', 'positive',
]
