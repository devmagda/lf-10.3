from .comments import CommentService
from .subscriptions import SubscriptionService
from app.models.event import Event
from .database import ConnectionUtil

connection = ConnectionUtil.from_global_config()


class EventService:
    @staticmethod
    def get_all_events():
        cursor = connection.db.cursor()
        cursor.execute("SELECT event_id, owner_username, title, title_short, description FROM event_owner_view")
        events = cursor.fetchall()
        all_events = []
        for event in events:
            if event[0] is not None and event[1] is not None and event[2] is not None and event[3] is not None and \
                    event[4] is not None:
                e = EventService.from_event_base_sql(event)
                all_events.append(e)
        cursor.close()
        return all_events

    @staticmethod
    def create_event(title_short, title, description, owner_id):
        cursor = connection.db.cursor()
        cursor.execute("""
            INSERT INTO tbl_events (owner, title_short, title, description) 
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (owner_id, title_short, title, description))

        # Fetch the ID of the newly created event
        event_id = cursor.fetchone()[0]
        connection.db.commit()
        cursor.close()

        return EventService.get_event(event_id)

    @staticmethod
    def subscribe(event_id, user_id):
        cursor = connection.db.cursor()
        cursor.execute("""
            INSERT INTO tbl_event_subscriptions (event_id, user_id) 
            VALUES (%s, %s)
        """, (event_id, user_id))
        connection.db.commit()
        cursor.close()

    @staticmethod
    def get_event(event_id):
        cursor = connection.db.cursor()
        cursor.execute(
            "SELECT event_id, owner_username, title, title_short, description FROM event_owner_view e WHERE e.event_id = %s",
            (event_id,))
        event = cursor.fetchone()
        e = EventService.from_event_base_sql(event)
        cursor.close()
        return e

    @staticmethod
    def get_event_ids():
        cursor = connection.db.cursor()
        cursor.execute("SELECT id FROM tbl_events ORDER BY id DESC")
        events = cursor.fetchall()
        cursor.close()
        return events

    @staticmethod
    def from_event_base_sql(event):
        event_id = event[0]
        owner_username = event[1]
        title = event[2]
        title_short = event[3]
        description = event[4]
        comments = CommentService.get_all_comments_for_event(event_id)
        subscriptions = SubscriptionService.get_all_subscriptions_for_event(event_id)
        e = Event(event_id, owner_username, title, title_short, description, subscriptions, comments)
        return e

    @classmethod
    def get_events_for_user(cls, user_id):
        cursor = connection.db.cursor()
        cursor.execute("SELECT event_id, owner_username, title, title_short, description FROM event_owner_view where user_id = %s", (user_id,))
        events = cursor.fetchall()
        events_for_user = []
        for event in events:
            if event[0] is not None and event[1] is not None and event[2] is not None and event[3] is not None and \
                    event[4] is not None:
                e = EventService.from_event_base_sql(event)
                events_for_user.append(e)
        cursor.close()
        return events_for_user
