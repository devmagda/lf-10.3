import pytest

from app.app import create_app

@pytest.fixture
def app():
    return create_app()

def test_app():
    app = create_app()
    assert app is not None

def test_blueprints_registered(app):
    # Check if the blueprints are registered
    blueprints = [bp.name for bp in app.blueprints.values()]
    expected_blueprints = ['auth', 'roles', 'global', 'views', 'events']  # List of blueprint names
    for blueprint in expected_blueprints:
        assert blueprint in blueprints