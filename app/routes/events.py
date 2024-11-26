from flask import Blueprint, jsonify, request, Response, redirect, url_for, render_template
from flask_login import login_required, current_user

from ..models import View
from ..services import SessionManager, EventService

events_blueprint = Blueprint('events', __name__, template_folder='./app/templates')

@events_blueprint.route('/subscribe', methods=['POST'])
@login_required
def post_subscribe():
    try:
        # Get event_id and user_id from the form
        event_id = request.form.get('event_id')

        # Check if event_id and user_id are provided
        if not event_id:
            return "event_id is required", 400

        # Call the function to subscribe
        EventService.subscribe(event_id, current_user.id)

        return redirect(url_for('global.index'))
    except Exception as e:
        return str(e), 500



@events_blueprint.route('/create', methods=['POST'])
@login_required
def get_post_create_event():
    title_short = request.form['title_short']
    title = request.form['title']
    description = request.form['description']
    owner_id = current_user.id

    event_id = EventService.create_event(title_short, title, description, owner_id)

    SessionManager.set_view(View.EVENT_SINGLE)
    SessionManager.set_focused_event_id(event_id)

    return redirect(url_for('global.index'))


@events_blueprint.route('/<int:event_id>', methods=['POST'])
@login_required
def get_event(event_id):
    SessionManager.set_focused_event_id(event_id)
    SessionManager.set_view(View.EVENT_SINGLE)
    return redirect(url_for('global.index'))