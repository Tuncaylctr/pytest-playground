import pytest
import os


@pytest.fixture
def temp_file():
    file_path = "temp_notes_file.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("Notes for pytest course\n")

    yield file_path

    # Teardown logic
    os.remove(file_path)


def test_file_starts_with_name(temp_file):
    with open(temp_file, "r") as f:
        contents = f.read()
    assert contents == "Notes for pytest course\n"


def test_file_write_task(temp_file):
    with open(temp_file, "a") as f:
        f.write("task_1")
    with open(temp_file, "r") as f:
        contents = f.read()
    assert contents == "Notes for pytest course\ntask_1"





class FakeDBConnection:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        print("[Setup] Connected to fake DB")

    def close(self):
        self.connected = False
        print("[Teardown] Closed fake DB connection")

    def fetch_user(self):
        if not self.connected:
            raise RuntimeError("Not connected to DB")
        return {"id": 1, "name": "Alice"}


@pytest.fixture
def db_connection():
    db = FakeDBConnection()
    db.connect()
    yield db
    db.close()


def test_fetch_user(db_connection):
    user = db_connection.fetch_user()
    assert user["name"] == "Alice"


def test_connection_is_active(db_connection):
    assert db_connection.connected is True

