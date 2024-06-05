from http import HTTPStatus

from pytest import mark
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


"""Доступность страниц для различных пользователей."""


@mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (
            lazy_fixture('home_url'),
            lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('detail_url'),
            lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('edit_url'),
            lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            lazy_fixture('delete_url'),
            lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            lazy_fixture('edit_url'),
            lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('delete_url'),
            lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('login_url'),
            lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('logout_url'),
            lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            lazy_fixture('signup_url'),
            lazy_fixture('client'),
            HTTPStatus.OK
        ),
    )
)
@mark.django_db
def test_pages_availability_for_anonymous_user(
    parametrized_client,
    url,
    expected_status
):
    assert parametrized_client.get(url).status_code == expected_status


"""При попытке перейти на страницу редактирования или
удаления комментария анонимный пользователь перенаправляется
на страницу авторизации."""


@mark.parametrize(
    'url',
    (lazy_fixture('delete_url'), lazy_fixture('delete_url')),
)
def test_redirects(client, login_url, url):
    assertRedirects(client.get(url), f'{login_url}?next={url}')
