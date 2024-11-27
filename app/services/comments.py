from .database import ConnectionUtil
from ..models.event import Comment

connection = ConnectionUtil.from_global_config()

class CommentService:
    @staticmethod
    def get_all_comments_for_event(event_id):
        cursor = connection.db.cursor()
        cursor.execute("SELECT comment_id, comment, comment_owner_username FROM event_with_comments_view WHERE event_id = %s ORDER BY event_with_comments_view.comment_id DESC", (event_id,))
        comments = cursor.fetchall()
        cursor.close()
        all_comments = []
        for comment in comments:
            if comment[0] is not None and comment[1] is not None and comment[2] is not None:
                c = Comment(comment[0], comment[1], comment[2])
                all_comments.append(c)
        return all_comments

    @staticmethod
    def create_comment(event_id, owner, comment):
        cursor = connection.db.cursor()
        cursor.execute(
            "INSERT INTO tbl_comments (event_id, owner, comment) VALUES (%s, %s, %s) RETURNING id",
            (event_id, owner, comment)
        )
        comment_id = cursor.fetchone()[0]
        connection.db.commit()
        cursor.close()
        return Comment(comment_id, comment, owner)
