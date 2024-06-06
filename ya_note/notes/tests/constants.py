from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class ConstantClass(TestCase):
    NOTE_SLUG = 'slug'
    NOTE_TITLE = 'Заголовок'
    NOTE_TEXT = 'Текст'
    DATA_TEXT = 'Текст заметки'
    DATA_TITLE = 'Заголовок заметки'
    DATA_SLUG = 'name_pk'
    HOME_URL = reverse('notes:home')
    ADD_URL = reverse('notes:add')
    EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
    DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
    DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
    LIST_URL = reverse('notes:list')
    SUCCESS_URL = reverse('notes:success')
    LOGIN_URL = reverse('users:login')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            author=cls.author,
            slug=cls.NOTE_SLUG,
        )
        cls.data = {
            'slug': cls.DATA_SLUG,
            'title': cls.DATA_TITLE,
            'text': cls.DATA_TEXT,
        }
        cls.urls = (
            cls.EDIT_URL,
            cls.DETAIL_URL,
            cls.DELETE_URL,
            cls.ADD_URL,
            cls.LIST_URL,
            cls.SUCCESS_URL,
            cls.LOGIN_URL,
            cls.LOGOUT_URL,
            cls.SIGNUP_URL,
            cls.HOME_URL,
        )
