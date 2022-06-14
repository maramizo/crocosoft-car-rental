import pytest
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from app import app

@pytest.fixture()
def _app():
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(_app):
    return _app.test_client()


@pytest.fixture()
def runner(_app):
    return _app.test_cli_runner()
