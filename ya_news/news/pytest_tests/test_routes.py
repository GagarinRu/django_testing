from http import HTTPStatus

from pytest import mark
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


HOME_URL = lazy_fixture('home_url')
DETAIL_URL = lazy_fixture('detail_url')
EDIT_URL = lazy_fixture('edit_url')
DELETE_URL = lazy_fixture('delete_url')
LOGIN_URL = lazy_fixture('login_url')
LOGOUT_URL = lazy_fixture('logout_url')
SIGNUP_URL = lazy_fixture('signup_url')


AUTHOR_CLIENT = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')
NOT_AUTHOR_CLIENT = lazy_fixture('not_author_client')


@mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (
            HOME_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            DETAIL_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            EDIT_URL,
            NOT_AUTHOR_CLIENT,
            HTTPStatus.NOT_FOUND
        ),
        (
            DELETE_URL,
            NOT_AUTHOR_CLIENT,
            HTTPStatus.NOT_FOUND
        ),
        (
            EDIT_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK
        ),
        (
            DELETE_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK
        ),
        (
            LOGIN_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            LOGOUT_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            SIGNUP_URL,
            CLIENT,
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
    """Доступность страниц для различных пользователей."""
    assert parametrized_client.get(url).status_code == expected_status


@mark.parametrize(
    'url',
    (EDIT_URL, DELETE_URL),
)
def test_redirects(client, login_url, url):
    """Доступность EDIT_URL и DELETE_URLдля анонимный пользователя."""
    assertRedirects(client.get(url), f'{login_url}?next={url}')
