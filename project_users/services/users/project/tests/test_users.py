from project import db
from project.api.models import User
import json
import unittest
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):

    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "michael",
                        "email": "michael@mherman.org",
                        "password": "greaterthaneight",
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("michael@mherman.org was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    # Fix missing comma in the next three methods
    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "michael@mherman.org"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            print(data)
            self.assertIn("Invalid payload", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "michael",
                        "email": "michael@mherman.org",
                        "password": "greaterthaneight",
                    }
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {
                        "username": "michael",
                        "email": "michael@mherman.org",
                        "password": "greaterthaneight",
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get a single user behaves correctly."""
        user = add_user("michael", "michael@mherman.org", "greaterthaneight")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("michael", data["data"]["username"])
            self.assertIn("michael@mherman.org", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    dict(
                        username="michael",
                        email="michael@reallynotreal.com",
                    )
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload", data["message"])
            self.assertEqual("fail", data["status"])


if __name__ == "__main__":
    unittest.main()
