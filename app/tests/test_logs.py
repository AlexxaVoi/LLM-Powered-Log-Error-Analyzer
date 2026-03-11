from fastapi import status


def test_get_list_logs(client):
    response = client.get("/log?user_id=1")

    assert response.status_code == status.HTTP_200_OK


def test_success_upload_raw(client):
    data = {
        "user_id": 1,
        "log_text": "ERROR Something went wrong"
    }

    response = client.post("/log/raw", json=data)

    assert response.status_code == status.HTTP_200_OK
