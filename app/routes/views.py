import os

from flask import Blueprint, redirect, url_for

from app.models import View
from app.services import SessionManager

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/<view_name>', methods=['POST', 'GET'])
def set_view(view_name):
    try:
        view = View(view_name)
        SessionManager.set_view(view)
    except ValueError:
        return "Invalid view", 404  # Handle invalid view names

    # Redirect to a default page or a page based on the view
    return redirect(url_for('global.index'))
