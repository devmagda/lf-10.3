# Corresponds to index_container.html

from enum import Enum

class View(Enum):
    HOME = 'home'
    LOGIN = 'login'
    REGISTER = 'register'
    TERMS = 'terms-and-conditions'
    IMPRINT = 'imprint'
    TEAM = 'team'
    EVENT_ALL = 'all-events'
    EVENT_SINGLE = 'single-event'
    EVENT_CREATE = 'event-create'