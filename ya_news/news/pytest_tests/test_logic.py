from http import HTTPStatus

from pytest import mark
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


"""Авторизованный пользователь может отправить комментарий."""


def test_user_can_create_news(author_client, author, form_data, detail_url):
    before_comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == before_comments_count + 1
    new_comment = Comment.objects.last()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


"""Анонимный пользователь не может отправить комментарий."""


@mark.django_db
def test_anonymous_user_cant_create_news(client, form_data, detail_url):
    before_comments_count = Comment.objects.count()
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == before_comments_count


"""Авторизованный пользователь может редактировать
свои комментарии."""


def test_author_can_edit_news(
    author_client,
    author, form_data,
    comment,
    edit_url,
    detail_url
):
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.get(id=comment.id).text == form_data['text']
    assert Comment.objects.get(id=comment.id).author == author
    assert Comment.objects.get(id=comment.id).news == comment.news


"""Авторизованный пользователь не может редактировать
чужие комментарии."""


def test_other_user_cant_edit_news(
        not_author_client,
        author,
        form_data,
        comment,
        edit_url
):
    before_comments_count = Comment.objects.count()
    response = not_author_client.post(edit_url, form_data)
    assert Comment.objects.count() == before_comments_count
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.get(id=comment.id).text == comment.text
    assert Comment.objects.get(id=comment.id).author == author
    assert Comment.objects.get(id=comment.id).news == comment.news


"""Авторизованный пользователь может удалять свои комментарии."""


def test_author_can_delete_news(author_client, detail_url, delete_url):
    before_comments_count = Comment.objects.count()
    response = author_client.post(delete_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == before_comments_count - 1


"""Авторизованный пользователь не может
или удалять чужие комментарии."""


def test_other_user_cant_delete_note(not_author_client, delete_url):
    before_comments_count = Comment.objects.count()
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == before_comments_count


"""Если комментарий содержит запрещённые слова, он не будет опубликован,
а форма вернёт ошибку."""


def test_user_cant_use_bad_words(author_client, detail_url):
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
