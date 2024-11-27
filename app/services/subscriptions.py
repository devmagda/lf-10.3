from .database import ConnectionUtil
from app.models.event import Subscription

connection = ConnectionUtil.from_global_config()


class SubscriptionService:
    @staticmethod
    def get_all_subscriptions_for_event(event_id):
        cursor = connection.db.cursor()
        cursor.execute("SELECT subscription_id, subscribed_username  FROM event_subscriptions WHERE event_id = %s",
                       (event_id,))
        subscriptions = cursor.fetchall()
        cursor.close()
        all_subscriptions = []
        for subscription in subscriptions:
            if subscription[0] is not None and subscription[1] is not None:
                s = Subscription(subscription[0], subscription[1])
                all_subscriptions.append(s)
        return all_subscriptions
