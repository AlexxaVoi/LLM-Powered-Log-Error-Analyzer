import io
from fastapi import status


def test_get_list_logs(client, auth):
    response = client.get("/log", auth=auth)
    assert response.status_code == status.HTTP_200_OK


def test_upload_raw_with_error(client, auth):
    data = {"log_text": "ERROR Something went wrong"}
    response = client.post("/log/raw", json=data, auth=auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["log_text"] == data["log_text"]


def test_upload_raw_without_errors(client, auth):
    data = {"log_text": "INFO: All is ok!"}
    response = client.post("/log/raw", json=data, auth=auth)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "No errors found in the provided log text"


def test_upload_file_success(client, auth, user):
    file_content = b"ERROR Database connection failed"
    response = client.post(
        "/log/upload",
        files={"file": ("log.txt", io.BytesIO(file_content), "text/plain")},
        auth=auth
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["user_id"] == user.id
    assert "ERROR" in body["log_text"]


def test_upload_file_invalid_format(client, auth):
    file_content = b"ERROR Database connection failed"
    response = client.post(
        "/log/upload",
        files={"file": ("log.pdf", io.BytesIO(file_content), "application/pdf")},
        auth=auth
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only .txt, .log and .csv files are allowed" in response.json()["detail"]
