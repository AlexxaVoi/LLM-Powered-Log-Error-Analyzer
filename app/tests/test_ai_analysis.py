from fastapi import status


def test_analysis_success(client, auth, log_in_db, mock_ai_analysis):
    mock_ai_analysis.return_value = {
        "issue": "Database Error",
        "root_cause": "Connection timeout",
        "solution": "Restart database"
    }
    response = client.post(f"/log/{log_in_db.id}/analysis", auth=auth)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["log_id"] == log_in_db.id
    assert body["issue"] == "Database Error"


def test_analysis_log_not_found(client, auth):
    response = client.post("/log/99999/analysis", auth=auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Log not found or access denied"


def test_analysis_ai_fail(client, auth, log_in_db, mock_ai_analysis):
    mock_ai_analysis.return_value = {"issue": "AI Analysis Failed"}

    response = client.post(f"/log/{log_in_db.id}/analysis", auth=auth)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "AI service is currently unavailable" in response.json()["detail"]
