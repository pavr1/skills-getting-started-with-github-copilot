from urllib.parse import quote


def activity_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name)}"


def test_get_activities(client):
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_participant_success(client):
    # Arrange
    email = "alice@mergington.edu"

    # Act
    response = client.post(
        f"{activity_path('Chess Club')}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Chess Club"
    }
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_participant_duplicate(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"{activity_path('Chess Club')}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    # Arrange
    email = "test.user@mergington.edu"

    # Act
    response = client.post(
        f"{activity_path('Nonexistent Activity')}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_success(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"{activity_path('Chess Club')}/participants?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Chess Club"
    }
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_participant_not_registered(client):
    # Arrange
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"{activity_path('Chess Club')}/participants?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_nonexistent_activity(client):
    # Arrange
    email = "test.user@mergington.edu"

    # Act
    response = client.delete(
        f"{activity_path('Nonexistent Activity')}/participants?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
