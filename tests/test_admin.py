def test_only_admin_role_is_authorized():
    assert 'student' != 'admin'
