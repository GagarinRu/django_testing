from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from .constants import ConstantClass

User = get_user_model()


class TestNotesPage(ConstantClass):
    """Отдельная заметка передаётся на страницу со списком заметок."""

    def test_notes_list_for_author(self):
        response = self.author_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertEqual(object_list.first().title, self.NOTE_TITLE)
        self.assertEqual(object_list.first().text, self.NOTE_TEXT)
        self.assertEqual(object_list.first().author, self.author)
        self.assertEqual(object_list.first().slug, self.NOTE_SLUG)

    """В список заметок одного пользователя не попадают
    заметки другого пользователя."""

    def test_notes_list_for_reader(self):
        response = self.reader_client.get(self.LIST_URL)
        self.assertEqual(response.context['object_list'].count(), 0)

    """Проверка, что на страницы создания и
    редактированиязаметки передаются формы."""

    def test_authorized_client_has_form(self):
        urls = (
            self.EDIT_URL,
            self.ADD_URL,
        )
        for url in urls:
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
