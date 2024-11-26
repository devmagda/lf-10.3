from ..models.event import Event
from .database import ConnectionUtil

connection = ConnectionUtil.from_global_config()

class EventService:
    @staticmethod
    def get_all_events():
        cursor = connection.db.cursor()
        cursor.execute("SELECT * FROM tbl_events")
        events = cursor.fetchall()
        cursor.close()
        return events

    @staticmethod
    def get_all_events_with_users():
        cursor = connection.db.cursor()
        cursor.execute("SELECT e.*, u.username FROM tbl_events e LEFT JOIN tbl_users u ON e.owner = u.id")
        events_users = cursor.fetchall()
        cursor.close()
        return events_users

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

        return event_id

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
    def get_event_by_id(event_id):
        cursor = connection.db.cursor()
        cursor.execute(
            "SELECT e.*, u.username FROM tbl_events e LEFT JOIN tbl_users u ON e.owner = u.id WHERE e.id = %s",
            (event_id,))
        event = cursor.fetchone()
        cursor.close()
        return event

    @staticmethod
    def get_event_ids():
        cursor = connection.db.cursor()
        cursor.execute("SELECT id FROM tbl_events ORDER BY id DESC")
        events = cursor.fetchall()
        cursor.close()
        return events

    @staticmethod
    def get_event_subscriptions(event_id):
        cursor = connection.db.cursor()
        cursor.execute(
            "select u.username from tbl_event_subscriptions s left join tbl_users u on s.user_id = u.id where s.event_id = %s",
            (event_id,))
        subscriptions = cursor.fetchall()
        cursor.close()
        return subscriptions

    @staticmethod
    def from_sql_data(event, subscriptions):
        id = event[0]
        owner_username = event[5]  # Owner's username is now in event[5] due to the LEFT JOIN
        title_short = event[2]
        title = event[3]
        description = event[4]

        # Convert the subscriptions tuples into a flat list of usernames
        subscription_list = [sub[0] for sub in subscriptions]

        return Event(id, owner_username, title, title_short, description, subscription_list)
