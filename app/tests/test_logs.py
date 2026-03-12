import io
from fastapi import status


def test_get_list_logs(client, user):
    response = client.get(f"/log?user_id={user.id}")
    assert response.status_code == status.HTTP_200_OK


def test_upload_raw_with_error(client, user):
    data = {
        "user_id": user.id,
        "log_text": "ERROR Something went wrong"
    }
    response = client.post("/log/raw", json=data)
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["log_text"] == data["log_text"]


def test_upload_raw_without_errors(client, user):
    data = {
        "user_id": user.id,
        "log_text": "INFO: All is ok!"
    }
    response = client.post("/log/raw", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body["detail"] == "No errors found in the provided log text"


def test_upload_file_success(client, user):
    file_content = b"ERROR Database connection failed"
    response = client.post(
        f"/log/upload?user_id={user.id}",
        files={"file": ("log.txt", io.BytesIO(file_content), "text/plain")}
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["user_id"] == user.id
    assert "ERROR" in body["log_text"]


def test_upload_file_invalid_format(client, user):
    file_content = b"ERROR Database connection failed"
    response = client.post(
        f"/log/upload?user_id={user.id}",
        files={"file": ("log.pdf", io.BytesIO(file_content), "application/pdf")}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body["detail"] == "Only .txt, .log and .csv files are allowed"
