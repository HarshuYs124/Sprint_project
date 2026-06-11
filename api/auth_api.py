class AuthAPI:

    def __init__(self, client):
        self.client = client

    def login(self, email, password):

        payload = {
            "email": email,
            "password": password
        }

        return self.client.post(
            "/users/login",
            payload
        )