import os

from flask import Blueprint, render_template

from app.models import UserRole
from app.models import View
from app.services import SessionManager, EventService

global_blueprint = Blueprint('global', __name__)


@global_blueprint.route('/')
def index():
    view_name = SessionManager.get_view().name
    role_id = SessionManager.get_user_role().value
    events = []
    focused_event_id = SessionManager.get_focused_event_id()
    focused_event = None

    if role_id >= UserRole.USER.value:
        events = EventService.get_all_events()

    if view_name == View.EVENT_SINGLE.name and focused_event_id is not None:
        focused_event = EventService.get_event(focused_event_id)

    return render_template('index.html', view=view_name, role=role_id, event_list=events, focused_event=focused_event)
