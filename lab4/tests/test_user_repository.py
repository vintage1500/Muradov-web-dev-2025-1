def test_get_by_id_with_nonexisting_user(user_repository):
    user = user_repository.get_by_id(100)
    assert user is None

def test_get_by_id_with_existing_user(user_repository, existing_users):
    user = user_repository.get_by_id(1)
    assert user["id"] == existing_users[0].id
    assert user["username"] == existing_users[0].username
    assert user["first_name"] == existing_users[0].first_name
    assert user["role_id"] == existing_users[0].role_id

def test_get_by_username_and_password_with_valid_data(user_repository, existing_users):
    user = user_repository.get_by_username_and_password('user1', 'password1')
    assert user["id"] == existing_users[0].id
    assert user["username"] == existing_users[0].username

def test_get_by_username_and_password_with_invalid_data(user_repository, existing_users):
    user = user_repository.get_by_username_and_password('user_none', 'password_none')
    assert user is None

def test_all_with_nonempty_db(user_repository, existing_users):
    users = user_repository.all()
    assert len(users) == len(existing_users)
    for loaded_user, existing_user in zip(users, existing_users):
        assert loaded_user["id"] == existing_user.id
        assert loaded_user["username"] == existing_user.username

def test_create_user(user_repository, existing_role):
    user_repository.create('newuser', 'newpassword', 'Daniel', 'Ulukov', 'Vladimirovich', existing_role.id)
    user = user_repository.get_by_username_and_password('newuser', 'newpassword')
    assert user is not None
    assert user["username"] == 'newuser'
    assert user['first_name'] == 'Daniel'

def test_update_user(user_repository, existing_users):
    user_repository.update(existing_users[0].id, "NewFirstName", "NewMiddleName", "NewLastName", existing_users[0].role_id)
    updated_user = user_repository.get_by_id(existing_users[0].id)
    assert updated_user["first_name"] == "NewFirstName"
    assert updated_user["middle_name"] == "NewMiddleName"
    assert updated_user["last_name"] == "NewLastName"

def test_delete_user(user_repository, existing_users):
    user_repository.delete(existing_users[0].id)
    deleted_user = user_repository.get_by_id(existing_users[0].id)
    assert deleted_user is None

def test_update_user_passwordd(user_repository, existing_users):
    user_repository.update_password(existing_users[0].id, "NewPassword")
    user = user_repository.get_by_username_and_password(existing_users[0].username, "NewPassword")
    assert user is not None

