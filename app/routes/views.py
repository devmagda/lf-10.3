import os

from flask import Blueprint, jsonify, request, Response, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models import UserRole
from app.models import View
from app.models.event import Event
from app.services import SessionManager, EventService

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/view/<view_name>', methods=['POST'])
def set_view(view_name):
    try:
        view = View(view_name)
        SessionManager.set_view(view)
    except ValueError:
        return "Invalid view", 404  # Handle invalid view names

    # Redirect to a default page or a page based on the view
    return redirect(url_for('global.index'))