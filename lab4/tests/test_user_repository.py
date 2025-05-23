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