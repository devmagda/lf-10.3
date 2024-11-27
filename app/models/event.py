from typing import List


class Event:
    def __init__(
            self,
            event_id: int,
            owner_username: str,
            title: str,
            title_short: str,
            description: str,
            subscriptions: List['Subscription'] = None,
            comments: List['Comment'] = None
    ) -> None:
        self.id: int = event_id
        self.owner_username: str = owner_username
        self.title: str = title
        self.title_short: str = title_short
        self.description: str = description
        self.subscriptions: List['Subscription'] = subscriptions or []
        self.comments: List['Comment'] = comments or []

    def get_subscriptions(self) -> str:
        return ', '.join(subscription.get_username() for subscription in self.subscriptions)

    def get_id(self) -> int:
        return self.id

    def get_comments(self) -> List['Comment']:
        return self.comments

    def get_title(self) -> str:
        return self.title

    def get_title_short(self) -> str:
        return self.title_short

    def get_description(self) -> str:
        return self.description

    def get_owner_username(self) -> str:
        return self.owner_username

    def has_comments(self) -> bool:
        return len(self.comments) > 0

    def has_subscriptions(self) -> bool:
        return len(self.subscriptions) > 0


class Comment:
    def __init__(self, comment_id: int, comment: str, username: str) -> None:
        self.comment_id: int = comment_id
        self.comment: str = comment
        self.username: str = username

    def get_comment(self) -> str:
        return self.comment

    def get_username(self) -> str:
        return self.username


class Subscription:
    def __init__(self, subscription_id: int, username: str) -> None:
        self.subscription_id: int = subscription_id
        self.username: str = username

    def get_username(self) -> str:
        return self.username
