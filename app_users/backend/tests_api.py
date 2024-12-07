import unittest
from unittest.mock import MagicMock
from controllers import Users
from models import DbUtils


class TestUsersController(unittest.TestCase):
    def setUp(self):
        self.mock_db_utils = MagicMock(spec=DbUtils)
        self.users_controller = Users(db_utils=self.mock_db_utils)

    def test_creating_user_success(self):
        self.mock_db_utils.execute_query.return_value = [
            ("existing_email@example.com",)
        ]
        response, status = self.users_controller.creating_user(
            "Test User", "test@test.com"
        )
        self.assertEqual(status, 200)
        self.assertIn("User added with success", response["message"])
        self.mock_db_utils.execute_query.assert_called()

    def test_creating_user_duplicate_email(self):
        self.mock_db_utils.execute_query.side_effect = [[("test@test.com",)], None]
        response, status = self.users_controller.creating_user(
            "Second test user", "test@test.com"
        )
        self.assertEqual(status, 400)
        self.assertIn("Email test@test.com used for another user", response["message"])

    def test_creating_user_invalid_payload(self):
        response, status = self.users_controller.creating_user("", "")
        self.assertEqual(status, 400)
        self.assertIn("Invalid payload", response["error"])

    def test_getting_users_success(self):
        self.mock_db_utils.execute_query.return_value = [
            {"id": 1, "name": "Test User", "email": "test@test.com"}
        ]
        response, status = self.users_controller.getting_users()
        self.assertEqual(status, 200)
        self.assertEqual(len(response), 1)

    def test_getting_users_no_data(self):
        self.mock_db_utils.execute_query.return_value = []
        response, status = self.users_controller.getting_users()
        self.assertEqual(status, 400)
        self.assertIn("No users found", response["message"])

    def test_get_one_user_by_id_success(self):
        self.mock_db_utils.execute_query.return_value = [
            {"id": 1, "name": "Test User", "email": "test@test.com"}
        ]
        response, status = self.users_controller.get_one_user_by_id("1")
        self.assertEqual(status, 200)
        self.assertIn("id", response)

    def test_get_one_user_by_id_not_found(self):
        self.mock_db_utils.execute_query.return_value = []
        response, status = self.users_controller.get_one_user_by_id("1")
        self.assertEqual(status, 400)
        self.assertIn("No users found", response["message"])

    def test_delete_one_user_by_id_success(self):
        self.mock_db_utils.execute_query.side_effect = [
            [{"id": 1, "name": "Test User", "email": "test@test.com"}],
            None,
        ]
        response, status = self.users_controller.delete_one_user_by_id("1")
        self.assertEqual(status, 200)
        self.assertIn("User with id 1 was deleted", response["message"])

    def test_delete_one_user_by_id_not_found(self):
        self.mock_db_utils.execute_query.return_value = []
        response, status = self.users_controller.delete_one_user_by_id("99")
        self.assertEqual(status, 400)
        self.assertIn("User id 99 not found", response["message"])

    def test_updating_user_by_id_success(self):
        self.mock_db_utils.execute_query.side_effect = [
            [{"id": 1, "name": "Test User", "email": "test@test.com"}],
            [("existing_email@example.com",)],
            None,  # Update query
        ]
        response, status = self.users_controller.updating_user_by_id(
            {"name": "Test Updated", "email": "test.updated@example.com"}, "1"
        )
        self.assertEqual(status, 200)
        self.assertIn("changed for id 1 with success", response["message"])

    def test_updating_user_by_id_invalid_payload(self):
        self.mock_db_utils.execute_query.side_effect = [
            [{"id": 1, "name": "Test User", "email": "test@test.com"}],
            [("existing_email@example.com",)],
        ]
        response, status = self.users_controller.updating_user_by_id({}, "1")
        self.assertEqual(status, 500)
        self.assertIn("Isn't a valid payload", response["error"])

    def test_updating_user_by_id_email_conflict(self):
        self.mock_db_utils.execute_query.side_effect = [
            [{"id": 1, "name": "Test User", "email": "test@test.com"}],
            [("test@test.com",)],
        ]
        response, status = self.users_controller.updating_user_by_id(
            {"email": "test@test.com"}, "1"
        )
        self.assertEqual(status, 400)
        self.assertIn("This email is alread set by other user", response["message"])


if __name__ == "__main__":
    unittest.main()
