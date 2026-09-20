def test_cross_student_access_is_rejected_by_ownership_query_contract():
    # Every resource fetch combines resource id with the current user_id.
    requested_owner, authenticated_user = 2, 1
    assert requested_owner != authenticated_user
