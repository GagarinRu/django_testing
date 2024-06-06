from http import HTTPStatus

from pytest import mark
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_can_create_news(author_client, author, form_data, detail_url):
    """Авторизованный пользователь может отправить комментарий."""
    before_comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == before_comments_count + 1
    new_comment = Comment.objects.last()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


pytestmark = mark.django_db


def test_anonymous_user_cant_create_news(client, form_data, detail_url):
    """Анонимный пользователь не может отправить комментарий."""
    before_comments_count = Comment.objects.count()
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == before_comments_count


def test_author_can_edit_news(
    author_client,
    author, form_data,
    comment,
    edit_url,
    detail_url
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, f'{detail_url}#comments')
    edit_comment = Comment.objects.get(id=comment.id)
    assert edit_comment.text == form_data['text']
    assert edit_comment.author == author
    assert edit_comment.news == comment.news


def test_other_user_cant_edit_news(
        not_author_client,
        author,
        form_data,
        comment,
        edit_url
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    before_comments_count = Comment.objects.count()
    response = not_author_client.post(edit_url, form_data)
    assert Comment.objects.count() == before_comments_count
    assert response.status_code == HTTPStatus.NOT_FOUND
    edit_comment = Comment.objects.get(id=comment.id)
    assert edit_comment.text == comment.text
    assert edit_comment.author == author
    assert edit_comment.news == comment.news


def test_author_can_delete_news(author_client, detail_url, delete_url):
    """Авторизованный пользователь может удалять свои комментарии."""
    before_comments_count = Comment.objects.count()
    response = author_client.post(delete_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == before_comments_count - 1


def test_other_user_cant_delete_note(not_author_client, delete_url):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    before_comments_count = Comment.objects.count()
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == before_comments_count


def test_user_cant_use_bad_words(author_client, detail_url):
    """Проверка комментария на запрещённые слова."""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    before_comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == before_comments_count
