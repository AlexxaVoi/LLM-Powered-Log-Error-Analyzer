from fastapi import status


def test_analysis_success(client, user, log_in_db, mock_ai_analysis):
    mock_ai_analysis.return_value = {
        "issue": "Database Error",
        "root_cause": "Connection timeout",
        "solution": "Restart database"
    }

    response = client.post(f"/log/{log_in_db.id}/analysis?user_id={user.id}")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["log_id"] == log_in_db.id
    assert body["issue"] == "Database Error"


def test_analysis_log_not_found(client, user):
    response = client.post(f"/log/99999/analysis?user_id={user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = response.json()
    assert body["detail"] == "Log not found or access denied"


def test_analysis_ai_fail(client, user, log_in_db, mock_ai_analysis):
    mock_ai_analysis.return_value = {"issue": "AI Analysis Failed"}

    response = client.post(f"/log/{log_in_db.id}/analysis?user_id={user.id}")
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    body = response.json()
    assert "AI service is currently unavailable" in body["detail"]
