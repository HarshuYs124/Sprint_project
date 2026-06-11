import pytest


@pytest.mark.order(7)
def test_delete_note_via_api(api_setup):
	"""End-to-end API test:
	1. Login via API (done by the `api_setup` fixture)
	2. Create a note via API
	3. Delete the created note via API
	4. Validate deletion status and that the note is gone from GET /notes
	"""
	notes_api = api_setup["notes"]
	token = api_setup["token"]

	# 2. Create a note (Pass the token)
	create_response = notes_api.create_note(
		token=token,
		title="Delete Test Note",
		description="Delete Test Description",
		category="Home",
	)

	assert create_response.status_code in [200, 201], (
		f"Failed to create note: {create_response.status_code} - {create_response.text}"
	)

	# Extract the dynamic note ID
	note = create_response.json().get("data")
	assert note and "id" in note, f"Create response missing note id: {create_response.json()}"
	note_id = note["id"]

	# 3. Delete the note using its ID (Pass the token)
	delete_response = notes_api.delete_note(note_id, token=token)
	assert delete_response.status_code in [200, 204], (
		f"Failed to delete note: {delete_response.status_code} - {delete_response.text}"
	)

	# 4. Message indicates successful deletion (if body returned)
	if delete_response.status_code == 204:
		# No content, consider this a success
		pass
	else:
		try:
			body = delete_response.json()
		except ValueError:
			body = None

		assert body, f"Delete response did not return JSON: {delete_response.text}"
		# Look for common success indicators
		msg = (
			body.get("message")
			or body.get("msg")
			or (body.get("data") and body.get("data").get("message"))
			or str(body)
		)
		assert any(k in msg.lower() for k in ("delete", "deleted", "success")), (
			f"Delete response message does not indicate success: {msg}"
		)

	# 5. Fetch all notes to verify it's gone (Pass the token)
	all_notes_response = notes_api.get_all_notes(token=token)
	assert all_notes_response.status_code == 200, (
		f"Failed to fetch notes after delete: {all_notes_response.status_code} - {all_notes_response.text}"
	)

	notes = all_notes_response.json().get("data", [])

	# 6. Verify the ID no longer exists in the system
	deleted_note = next((n for n in notes if n.get("id") == note_id), None)

	assert deleted_note is None, f"Defect: Note with ID {note_id} still exists in backend!"
