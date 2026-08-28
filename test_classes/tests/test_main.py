import pytest

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

class TestDocumentEditor:
    def test_write(self):
        editor = DocumentEditor()
        editor.write('some text')
        assert editor.content == 'some text'

    def test_clear(self):
        editor = DocumentEditor()
        editor.write('some text')
        editor.clear()
        assert editor.is_empty()

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



