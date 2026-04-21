from src import app as app_module


def test_get_activities_returns_seeded_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert "participants" in data[expected_activity]


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_case_insensitive_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email_different_case = "MICHAEL@MERGINGTON.EDU"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email_different_case},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Debate Club"
    email = "notfound@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_case_insensitive_match_removes_original_entry(client):
    # Arrange
    activity_name = "Chess Club"
    submitted_email = "MICHAEL@MERGINGTON.EDU"
    original_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": submitted_email},
    )

    # Assert
    assert response.status_code == 200
    participants = app_module.activities[activity_name]["participants"]
    assert original_email not in participants
    assert response.json()["message"] == f"Unregistered {original_email} from {activity_name}"
