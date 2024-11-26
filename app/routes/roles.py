from flask import Blueprint

from ..services import RoleService

roles_blueprint = Blueprint('roles', __name__, template_folder='./app/templates')

@roles_blueprint.route('/roles', methods=['GET'])
def get_get_roles():
    events = RoleService.get_all_roles()
    return events