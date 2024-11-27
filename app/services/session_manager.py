from flask import session
from ..models import UserRole, View


class SessionManager:

    @staticmethod
    def set_focused_event_id(event_id):
        session['focused_event_id'] = event_id

    @staticmethod
    def get_focused_event_id():
        view_value = session.get('focused_event_id', None)
        return view_value

    @staticmethod
    def set_view(view: View):
        session['view'] = view.value  # Store only the value of the enum

    @staticmethod
    def get_view():
        view_value = session.get('view', View.HOME.value)  # Default to HOME if 'view' is not set
        return View(view_value)  # Convert the stored value back to a View enum

    @staticmethod
    def get_user_role():
        return UserRole.get_by_id(session.get('role', UserRole.GUEST.value))

    @staticmethod
    def set_user_role(role: UserRole):
        session['role'] = role.value
