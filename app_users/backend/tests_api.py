import pytest
from unittest.mock import MagicMock
from controllers import Users  

@pytest.fixture
def mock_db_utils():
    mock = MagicMock()
    mock.get_db.return_value = MagicMock()
    return mock

def test_creating_user_success(mock_db_utils):

    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []  

    user_service = Users(mock_db_utils)

    name = "Teste User"
    email = "teste@example.com"
    msg, status = user_service.creating_user(name, email)

    assert status == 200
    assert msg == {"message": "User added with success for email teste@example.com "}

def test_creating_user_email_exists(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = [("teste@example.com",)]  # Email já no banco

    user_service = Users(mock_db_utils)

    name = "Jane Doe"
    email = "teste@example.com"
    msg, status = user_service.creating_user(name, email)

    assert status == 400
    assert msg == {"message": "Email teste@example.com used for another user "}

def test_getting_users_no_users(mock_db_utils):

    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []

    user_service = Users(mock_db_utils)

    msg, status = user_service.getting_users()

    assert status == 400
    assert msg == {"message": "No users found"}

def test_get_one_user_by_id_not_found_and_dict_empty(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []  

    user_service = Users(mock_db_utils)

    user_id = "12"
    msg, status = user_service.get_one_user_by_id(user_id)

    assert status == 400
    assert msg == {"message": "No users found"}

def test_deleting_user_success(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = [("1", "Teste User", "teste@example.com")]  # Usuário encontrado

    user_service = Users(mock_db_utils)
    user_id = "1"
    msg, status = user_service.delete_one_user_by_id(user_id)

    assert status == 200
    assert msg == {"message": "User with id 1 was deleted with success"}

def test_deleting_user_not_found(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []

    user_service = Users(mock_db_utils)
    user_id = "999"
    msg, status = user_service.delete_one_user_by_id(user_id)

    assert status == 400
    assert msg == {"message": "User id 999 not found"}

def test_updating_user_success(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.side_effect = [
        [("1", "Teste User", "teste@example.com")],
        []
    ]
    user_service = Users(mock_db_utils)
    user_id = "1"
    payload = {"name": "Joao Updated", "email": "Joao.updated@example.com"}
    msg, status = user_service.updating_user_by_id(payload, user_id)

    assert status == 200
    assert msg == {"message": "Keys name and email changed for id 1 with success"}

def test_updating_user_email_conflict(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.side_effect = [
        [("teste@example.com")],  
        [("jane@example.com",)]  
    ]

    user_service = Users(mock_db_utils)

    user_id = "1"
    payload = {"name": "Joao Updated", "email": "jane@example.com"}
    msg, status = user_service.updating_user_by_id(payload, user_id)

    assert status == 400
    assert msg == {"message": "This email is alread set by other user"}

def test_updating_user_invalid_payload(mock_db_utils):
    mock_conn = mock_db_utils.get_db.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = []  

    user_service = Users(mock_db_utils)

    user_id = "999"
    payload = {"name": "Joao Updated", "email": "Joao.updated@example.com"}
    msg, status = user_service.updating_user_by_id(payload, user_id)

    assert status == 500
    assert msg == {"error": "Invalid id"}

