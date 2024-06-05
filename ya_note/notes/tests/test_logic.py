from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .constants import ConstantClass

User = get_user_model()


class TestNotesLogic(ConstantClass):
    """Анонимный пользователь не может создать заметку."""

    def test_anonymous_user_cant_create_note(self):
        before_notes_count = Note.objects.count()
        self.client.post(self.ADD_URL, data=self.data)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count)

    """Залогиненный пользователь может создать заметку."""

    def test_user_can_create_notes(self):
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

    """Невозможность создания двух заметок с одинаковым slug."""

    def test_slug_unique(self):
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

    """Если при создании заметки не заполнен slug,
    то он формируется автоматически."""

    def test_slug_empty(self):
        self.data.pop('slug')
        Note.objects.all().delete()
        before_notes_count = Note.objects.count()
        response = self.author_client.post(self.ADD_URL, data=self.data)
        self.assertRedirects(response, self.SUCCESS_URL)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count + 1)
        self.assertEqual(Note.objects.get().slug, slugify(self.data['title']))
        self.assertEqual(Note.objects.get().title, self.data['title'])
        self.assertEqual(Note.objects.get().text, self.data['text'])
        self.assertEqual(Note.objects.get().author, self.author)

    """Пользователь может удалять свои заметки."""

    def test_author_can_delete_note(self):
        before_notes_count = Note.objects.count()
        response = self.author_client.delete(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCESS_URL)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count - 1)

    """Пользователь не может удалять чужие заметки."""

    def test_user_cant_delete_note_of_another_user(self):
        before_notes_count = Note.objects.count()
        response = self.reader_client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        after_notes_count = Note.objects.count()
        self.assertEqual(after_notes_count, before_notes_count)

    """Пользователь может редактировать свои заметки."""

    def test_author_can_edit_note(self):
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        response = self.author_client.post(self.EDIT_URL, data=self.data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note = Note.objects.get()
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.author, self.author)

    """Пользователь не может редактировать чужие заметки."""

    def test_user_cant_edit_note_of_another_user(self):
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        response = self.reader_client.post(self.EDIT_URL, data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get()
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.author)
