
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team for practices and matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Casual and competitive basketball sessions",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and school play productions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 30,
        "participants": ["ethan@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills; compete in debates",
        "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions across multiple disciplines",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # 各テスト前にactivitiesを初期状態にリセット
    for k in list(activities.keys()):
        del activities[k]
    for k, v in ORIGINAL_ACTIVITIES.items():
        activities[k] = {**v, "participants": list(v["participants"])}

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]

def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Programming Class"
    # Add participant first
    resp_signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_signup.status_code == 200
    # URLエンコードして削除
    from urllib.parse import quote
    encoded_email = quote(email)
    response = client.delete(f"/activities/{activity}/participants/{encoded_email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # Remove again should fail
    response_fail = client.delete(f"/activities/{activity}/participants/{encoded_email}")
    assert response_fail.status_code == 404
    assert "Participant not found" in response_fail.json()["detail"]

def test_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    response = client.delete("/activities/Nonexistent/participants/someone@mergington.edu")
    assert response.status_code == 404
