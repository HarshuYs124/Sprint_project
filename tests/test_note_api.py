import time

import pytest


@pytest.mark.order(5)
def test_get_notes(api_setup):

    config = api_setup["config"]

    login_response = api_setup["auth"].login(
        config["api"]["email"],
        config["api"]["password"]
    )

    print(login_response.json())

    assert login_response.status_code == 200

    token = login_response.json()["data"]["token"]

    start_time = time.time()

    notes_response = api_setup["notes"].get_notes(token)

    response_time = time.time() - start_time

    assert notes_response.status_code == 200
    assert response_time < 2

    notes = notes_response.json()["data"]

    assert isinstance(notes, list)

    print(notes)