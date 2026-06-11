import pytest
from pages.home_page import HomePage

@pytest.mark.order(6)
def test_validate_note_ui_vs_api(setup_and_teardown, api_setup):
    # 1. Initialize the UI Home Page using the driver
    hp = HomePage(setup_and_teardown)

    # 2. Grab the note details currently visible on the screen
    ui_title = hp.get_note_title()
    ui_description = hp.get_note_description()

    # 3. Get the API service and authentication token from your setup
    notes_api = api_setup["notes"]
    token = api_setup["token"]

    # 4. Make the API Call to get all notes
    response = notes_api.get_notes(token)
    assert response.status_code == 200, "API request failed!"

    # 5. Extract the list of notes from the API response data envelope
    notes_list = response.json()["data"]

    # 6. Find the note from the API that matches what we saw on the UI
    matching_note = next(
        (note for note in notes_list
         if note["title"] == ui_title and note["description"] == ui_description),
        None
    )

    # 7. Assertions: Verify the note actually exists and fields match
    assert matching_note is not None, f"UI Note '{ui_title}' was not found in the API backend!"
    assert matching_note["title"] == ui_title
    assert matching_note["description"] == ui_description
    assert matching_note["created_at"] is not None
    assert "completed" in matching_note
