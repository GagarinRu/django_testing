from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from .constants import ConstantClass

User = get_user_model()


class TestNotesPage(ConstantClass):
    def test_notes_list_for_author(self):
        """Отдельная заметка передаётся на страницу со списком заметок."""
        response = self.author_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        respone = object_list.first()
        self.assertEqual(respone.title, self.note.title)
        self.assertEqual(respone.text, self.note.text)
        self.assertEqual(respone.author, self.note.author)
        self.assertEqual(respone.slug, self.note.slug)

    def test_notes_list_for_reader(self):
        """Список заметок для разных пользователей."""
        response = self.reader_client.get(self.LIST_URL)
        self.assertEqual(response.context['object_list'].count(), 0)

    def test_authorized_client_has_form(self):
        urls = (
            self.EDIT_URL,
            self.ADD_URL,
        )
        """Страницы создания и редактированиязаметки передаются формы."""
        for url in urls:
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
