import pytest
#pytest tests/test_main.py -v
from test_classes.src import DocumentEditor
#before test-class-implementation

# def test_write():
#     editor = DocumentEditor()
#     editor.write('some text')
#     assert editor.content == 'some text'
#
# def test_clear():
#     editor = DocumentEditor()
#     editor.write('some text')
#     editor.clear()
#     assert editor.is_empty()

#pytest tests/test_main.py::TestDocumentEditor -v
class TestDocumentEditor:
    # pytest tests/test_main.py::TestDocumentEditor::test_write -v
    # pytest -k "write or clear" -v
    # pytest -k 'not empty_editor and  (write or clear)' -v
    def test_write(self):
        editor = DocumentEditor()
        editor.write('some text')
        assert editor.content == 'some text'

    def test_clear(self):
        editor = DocumentEditor()
        editor.write('some text')
        editor.clear()
        assert editor.is_empty()
    # pytest -m "smoke" -v
    @pytest.mark.smoke
    def test_get_last_content(self):
        editor = DocumentEditor()
        editor.write('some new text')
        editor.clear()

        expected_last_content = 'some new text'
        last_content = editor.get_last_content()

        error_msg = (f'Last content is expected to be '
                     f'the content before last operation.'
                     f'Actual editor history {editor.history};'
                     f'error: {expected_last_content=} vs. '
                     f'{last_content=}')

        assert last_content == expected_last_content,error_msg
        # if last_content != expected_last_content:
        #     pytest.fail(error_msg)

    def test_raise_error_if_no_history(self):
        editor = DocumentEditor()

        # with pytest.raises(ValueError,
        #                    match='No document history available:'):
        #     editor.get_last_content()

        with pytest.raises(ValueError) as excinfo:
            editor.get_last_content()
            assert str(excinfo.value).startswith('No document history available:')
            assert excinfo.type == ValueError

    def test_multiple_scenarios_at_once(self):
        editor = DocumentEditor()

        assert editor.is_empty()
        assert len(editor.history) == 0

        editor.clear()
        assert editor.is_empty()
        assert len(editor.history) == 1

        editor.write('Some line of text. ')
        editor.write('Next sentence here!')
        assert editor.content == 'Some line of text. Next sentence here!'
        assert not editor.is_empty()

    def test_initial_editor_is_empty(self):
        # GIVEN: initial document editor right after initialization (with no operations applied)
        editor = DocumentEditor()

        # WHEN: checking if the editor is empty
        is_editor_empty = editor.is_empty()

        # THEN: empty editor should be True, and history should also be empty
        assert is_editor_empty
        assert len(editor.history) == 0

    def test_clear_empty_editor_is_empty(self):
        # GIVEN: initial document editor right after initialization (with no operations applied)
        editor = DocumentEditor()

        # WHEN: clearing initial (empty) editor
        editor.clear()

        # THEN: editor should be empty, and the number of operations should be 1
        expected_number_of_operations = 1

        assert editor.is_empty()
        assert len(editor.history) == expected_number_of_operations

    def test_written_content_is_correct(self):
        # GIVEN: document editor
        editor = DocumentEditor()

        # WHEN: writing content to the document with multiple write operations
        editor.write('Some line of text. ')
        editor.write('Next sentence here!')

        # THEN: the content should be joined content from write operations
        assert editor.content == 'Some line of text. Next sentence here!'
        assert not editor.is_empty()


# pytest -m "smoke" -v
@pytest.mark.smoke
def test_dummy():
    assert  True

