from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Basic sanity checks
    assert "Programming Class" in data
    assert "participants" in data["Programming Class"]


def test_signup_and_unregister_flow():
    activity = "Programming Class"
    test_email = "testuser@example.com"

    # Ensure clean state: remove email if already present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up should succeed
    resp_signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_signup.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Signing up again should fail (already signed up)
    resp_duplicate = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_duplicate.status_code == 400

    # Unregister should succeed
    resp_delete = client.delete(f"/activities/{activity}/signup?email={test_email}")
    assert resp_delete.status_code == 200
    assert test_email not in activities[activity]["participants"]

    # Deleting again should return 404
    resp_delete_again = client.delete(f"/activities/{activity}/signup?email={test_email}")
    assert resp_delete_again.status_code == 404
