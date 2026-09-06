import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 5]


def test_sum(sample_data):
    actual_sum = sum(sample_data)
    expected_sum = 8
    assert actual_sum == expected_sum


def test_len(sample_data):
    actual_len = len(sample_data)
    expected_len = 3
    assert actual_len == expected_len


@pytest.fixture
def first_name():
    return 'Joe'


@pytest.fixture()
def last_name():
    return 'Smith'


@pytest.fixture()
def item():
    return 'an apple'


@pytest.fixture()
def full_sentence(first_name, last_name, item):
    return f"{first_name} {last_name} has {item}"


def test_sentence_full_is_correct(full_sentence):
    expected_sentence = "Joe Smith has an apple"
    assert full_sentence == expected_sentence


def test_sentence_has_word_has(full_sentence):
    assert 'has' in full_sentence
