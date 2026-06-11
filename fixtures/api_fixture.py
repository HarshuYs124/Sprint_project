import pytest

from Config.environment import ConfigReader
from api.api_client import APIClient
from api.auth_api import AuthAPI
from api.notes_api import NotesAPI


@pytest.fixture
def api_setup():
    # 1. Load the environment configuration
    config = ConfigReader.read_config()

    # 2. Initialize the base API Client
    client = APIClient(config["api"]["base_url1"])

    # 3. Instantiate the API domain objects
    auth_api = AuthAPI(client)
    notes_api = NotesAPI(client)

    # 4. Extract credentials and perform the login handshake background process
    email = config["qa"]["email"]
    password = config["qa"]["password"]

    login_response = auth_api.login(email, password)
    assert login_response.status_code == 200, f"Fixture Setup Failure: API Login failed with status {login_response.status_code}"

    # 5. Extract the authorization token safely
    token = login_response.json()["data"]["token"]

    # 6. Return everything your test file needs to execute cleanly
    return {
        "config": config,
        "auth": auth_api,
        "notes": notes_api,
        "token": token
    }

