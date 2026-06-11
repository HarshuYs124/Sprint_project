# Tell pytest to load fixtures from your custom directory module
pytest_plugins = [
    "fixtures.browser_fixture",
    "fixtures.api_fixture",
]
from fixtures.api_fixture import *
from fixtures.browser_fixture import *