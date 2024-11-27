from enum import Enum


class View(Enum):
    HOME: str = 'home'
    LOGIN: str = 'login'
    REGISTER: str = 'register'
    TERMS: str = 'terms-and-conditions'
    IMPRINT: str = 'imprint'
    TEAM: str = 'team'
    EVENT_ALL: str = 'all-events'
    EVENT_SINGLE: str = 'single-event'
    EVENT_CREATE: str = 'event-create'
    MY_EVENTS: str = 'my-events'
