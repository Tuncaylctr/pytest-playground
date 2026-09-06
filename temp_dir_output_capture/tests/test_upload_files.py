from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture(scope='session')
# tmp_path_factory allows session scope (tmp_path is function-scoped only)
#tmp_path_factory - .mktemp() to create folders , tmp_path	auto-created
def tmp_file(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('user_data')
    tmp_file = tmp_path / 'test_user_data.txt'
    tmp_file.write_text('Hello World!')
    yield tmp_file


def test_upload_successful(client, tmp_file):
    with tmp_file.open("rb") as f:
        response = client.post(
            "/user/123/file",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert response.status_code == 200


def test_upload_has_expected_response(client, tmp_file):
    with tmp_file.open("rb") as f:
        response = client.post(
            "/user/123/file",
            files={"file": ("test.txt", f, "text/plain")}
        )

    json_resp = response.json()

    assert json_resp["user_id"] == 123
    assert json_resp["filename"] == "test.txt"
    assert json_resp["content"] == "Hello World!"


def test_upload_logs(tmp_file, client, capsys):
    with tmp_file.open("rb") as f:
        response = client.post(
            "/user/123/file",
            files={"file": ("test.txt", f, "text/plain")}
        )
        captured = capsys.readouterr()
        assert "Received file: test.txt from user 123" in captured.out


# def test_upload_logs(client, tmp_file, caplog):
#     with caplog.at_level(logging.INFO):
#         with tmp_file.open("rb") as f:
#             response = client.post(
#                 "/user/123/file",
#                 files={"file": ("test.txt", f, "text/plain")}
#             )
#
#     assert "Received file: test.txt from user 123" in caplog.messages
