from http import HTTPStatus
import pytest

from pytest_django.asserts import assertFormError, assertRedirects
from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_can_create_news(author_client, author, form_data, comment):
    url = reverse('news:detail', args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 2
    new_comment = Comment.objects.last()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_news(client, comment, form_data):
    url = reverse('news:detail', args=(comment.id,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 1


def test_author_can_edit_news(author_client, author, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    url_done = reverse('news:detail', args=(comment.id,))
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{url_done}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author


def test_other_user_cant_edit_news(
        not_author_client,
        author,
        form_data,
        comment
):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == author


def test_author_can_delete_news(author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    url_done = reverse('news:detail', args=(comment.id,))
    response = author_client.post(url)
    assertRedirects(response, f'{url_done}#comments')
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, comment):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(comment.id,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 1
