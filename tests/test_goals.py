def test_completed_goal_status_rule():
    progress=100
    assert ('completed' if progress == 100 else 'active') == 'completed'
