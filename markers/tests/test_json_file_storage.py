from pathlib import Path

import pytest

from pftracker import JsonFileStorage

pytestmark = pytest.mark.markers_demo


@pytest.fixture
def fixed_pid(mocker):
    mocker.patch("os.getpid", return_value=12345)

@pytest.mark.critical
@pytest.mark.usefixtures("fixed_pid")
def test_lockfile_contains_pid(tmp_path):
    storage_path = tmp_path / "state.json"
    with JsonFileStorage(storage_path):
        pid = Path(str(storage_path) + ".lock").read_text().strip()
    assert pid == "12345"


# @pytest.mark.filterwarnings("ignore::UserWarning")
@pytest.mark.filterwarnings("ignore:.*Large JSON payload.*")
@pytest.mark.filterwarnings("error")
def test_saving_large_files(tmp_path, mocker):
    mocker.patch("pftracker.JsonFileStorage.SOFT_LIMIT_MB", new=0.01)
    storage_path = tmp_path / "state.json"
    with JsonFileStorage(storage_path) as storage:
        storage.save(payload={str(i): i for i in range(1000)})

pytest.mark.critical
@pytest.mark.xfail(
    reason="Reserving the same object twice with the same owner "
    "unexpectedly raises an error."
)
def test_second_instance_cannot_acquire_lock(tmp_path):
    path = tmp_path / "state.json"
    storage = JsonFileStorage(path)

    storage_holder = "Process 1"
    storage.reserve(owner=storage_holder)
    storage.reserve(owner=storage_holder)


#NOT A GOOD PRACTICE
@pytest.mark.xfail(
    reason="If a previous storage instance was not properly closed, "
    "the lock file remains and prevents reuse. "
    "Maybe we should later add a `force` flag to override."
)
def test_second_instance_cannot_acquire_lock(tmp_path):
    path = tmp_path / "state.json"
    JsonFileStorage(path)
    # maybe a crash or a forgotten .close(): lockfile never released

    JsonFileStorage(path)  # fails because lock is still held



#anothet usecase
# class TestDefaultCurrency:
#     @pytest.mark.critical
#     @pytest.mark.parametrize(
#         "currency",
#         [
#             pytest.param("USD", marks=pytest.mark.markers_demo),
#             pytest.param("EUR", marks=pytest.mark.skip),
#             "JPY",
#         ]
#     )


@pytest.mark.with_transactions
def test_tracker_with_transactions(tracker):
    assert len(tracker.list_transactions()) > 0


@pytest.mark.with_categories(["c1", "c2", "c3"])
def test_tracker_with_categories(tracker):
    assert tracker.list_categories() == ["c1", "c2", "c3"]