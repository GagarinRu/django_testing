from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, news_object',
    (
        ('news:home', None),
        ('news:detail', lazy_fixture('pk_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, news_object):
    url = reverse(name, args=news_object)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_redirects(client, comment, name,):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
