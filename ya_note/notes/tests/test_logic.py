from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .constants import ConstantClass

User = get_user_model()


class TestNotesLogic(ConstantClass):
    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        before_notes_count = Note.objects.count()
        self.client.post(self.ADD_URL, data=self.data)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count)

    def test_user_can_create_notes(self):
        """Залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        before_notes_count = Note.objects.count()
        response = self.author_client.post(self.ADD_URL, data=self.data)
        self.assertRedirects(response, self.SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, before_notes_count + 1)
        note = Note.objects.last()
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.author, self.author)

    def test_slug_unique(self):
        """Невозможность создания двух заметок с одинаковым slug."""
        slug_data = {'slug': self.NOTE_SLUG}
        before_notes_count = Note.objects.count()
        response = self.author_client.post(self.ADD_URL, data=slug_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count)

    def test_slug_empty(self):
        """Формирование slug при его отсутсвии при создании заметки."""
        self.data.pop('slug')
        Note.objects.all().delete()
        before_notes_count = Note.objects.count()
        response = self.author_client.post(self.ADD_URL, data=self.data)
        self.assertRedirects(response, self.SUCCESS_URL)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count + 1)
        respone = Note.objects.get()
        self.assertEqual(respone.slug, slugify(self.data['title']))
        self.assertEqual(respone.title, self.data['title'])
        self.assertEqual(respone.text, self.data['text'])
        self.assertEqual(respone.author, self.author)

    def test_author_can_delete_note(self):
        """Пользователь может удалять свои заметки."""
        before_notes_count = Note.objects.count()
        response = self.author_client.delete(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCESS_URL)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        """Пользователь не может удалять чужие заметки."""
        before_notes_count = Note.objects.count()
        response = self.reader_client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        response = self.author_client.post(self.EDIT_URL, data=self.data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note = Note.objects.get()
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может редактировать чужие заметки."""
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        response = self.reader_client.post(self.EDIT_URL, data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get()
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
