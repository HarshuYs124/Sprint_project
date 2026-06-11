class NotesAPI:

    def __init__(self, client):
        self.client = client

    def get_all_notes(self, token=None):
        headers = {"x-auth-token": token} if token else None
        return self.client.get("/notes", headers=headers)

    # Backwards compatible alias
    def get_notes(self, token=None):
        return self.get_all_notes(token)

    def delete_note(self, note_id, token=None):
        """Delete a note by id. Token is optional if client already has session-based auth."""
        headers = {"x-auth-token": token} if token else None
        return self.client.delete(f"/notes/{note_id}", headers=headers)

    def create_note(self, token, title, description, category):
        headers = {
            "x-auth-token": token
        }

        payload = {
            "title": title,
            "description": description,
            "category": category
        }

        return self.client.post(
            "/notes",

            payload=payload,
            headers=headers
        )