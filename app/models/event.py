class Event:
    def __init__(self, id, owner_username, title, title_short, description, subscriptions=None):
        self.id = id
        self.owner_username = owner_username
        self.title = title
        self.title_short = title_short
        self.description = description
        self.subscriptions = subscriptions if subscriptions is not None else []

    def get_subscriptions(self):
        return ', '.join(self.subscriptions)

    def get_id(self):
        return self.id
