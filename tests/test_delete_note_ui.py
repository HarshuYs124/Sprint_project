from pages.notes_page import NotesPage
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import pytest

@pytest.mark.order(8)
def test_deleted_note_disappears_from_ui(login_fixture, api_setup):
    """End-to-end UI test for note deletion:

    """
    driver = login_fixture
    notes_api = api_setup["notes"]
    token = api_setup["token"]

    # 1. Initialize page objects
    notes_page = NotesPage(driver)

    # Verify logged-in user can see the "Add Note" button
    assert notes_page.is_add_note_button_visible(), (
        "Add Note button is not visible - user may not be logged in properly"
    )

    # 2. Create note via API
    create_response = notes_api.create_note(
        token=token,
        title="Delete Through API",
        description="Delete Validation Test",
        category="Home",
    )

    assert create_response.status_code in [200, 201], (
        f"Failed to create note: {create_response.status_code} - {create_response.text}"
    )

    note = create_response.json().get("data")
    assert note and "id" in note, f"Create response missing note id: {create_response.json()}"

    note_id = note["id"]
    note_title = note.get("title", "Delete Through API")

    # 3. Delete note via API
    delete_response = notes_api.delete_note(note_id, token=token)
    assert delete_response.status_code in [200, 204], (
        f"Failed to delete note: {delete_response.status_code} - {delete_response.text}"
    )

    # 4. Verify deletion via API (GET /notes should not return the deleted note)
    all_notes_response = notes_api.get_all_notes(token=token)
    assert all_notes_response.status_code == 200
    notes_data = all_notes_response.json().get("data", [])

    deleted_from_api = next((n for n in notes_data if n.get("id") == note_id), None)
    assert deleted_from_api is None, f"Note {note_id} still exists in API after deletion!"

    # 5. Refresh page using driver.refresh() (or JS window.location.reload)
    sleep(1)  # brief pause to ensure backend sync
    notes_page.refresh_page()
    sleep(2)  # wait for page to load after refresh

    # 6. Validate note disappears from UI DOM
    # Extract all note titles with retry logic to handle potential stale elements
    note_titles = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            note_titles = notes_page.get_all_note_titles()
            break  # Success, exit retry loop
        except StaleElementReferenceException:
            if attempt < max_retries - 1:
                sleep(1)  # brief pause before retry
                continue
            else:
                raise  # Re-raise if all retries exhausted

    assert note_titles is not None, "Failed to extract note titles from UI after refresh"
    print(f"Current note titles in UI: {note_titles}")

    # 7. Confirm deleted note does not appear in UI
    assert note_title not in note_titles, (
        f"Defect: Note '{note_title}' still appears in UI after deletion! "
        f"Current titles: {note_titles}"
    )

    # 8. Validate no ghost entries: ensure clean DOM
    assert isinstance(note_titles, list), "Note titles should be a list"
    assert all(isinstance(title, str) for title in note_titles), (
        "All note titles should be strings"
    )

    # 9. Verify UI rendered correctly by checking the page contains expected elements
    # Try to fetch titles again to ensure DOM is stable (no broken UI)
    note_titles_recheck = notes_page.get_all_note_titles()
    assert note_titles == note_titles_recheck, (
        "Note titles changed between two successive reads - DOM may be unstable or broken"
    )
