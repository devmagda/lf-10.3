from . import ConnectionUtil

connection = ConnectionUtil.from_global_config()

class RoleService:
    @staticmethod
    def get_all_roles():
        cursor = connection.db.cursor()
        cursor.execute("SELECT * FROM ref_roles")
        events = cursor.fetchall()
        cursor.close()
        return events

    @staticmethod
    def get_selectable_roles():
        cursor = connection.db.cursor()
        cursor.execute("SELECT * FROM ref_roles where id in (1, 2)")
        events = cursor.fetchall()
        cursor.close()
        return events
