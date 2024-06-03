import pytest

from pytest_lazyfixture import lazy_fixture
from django.urls import reverse
from django.conf import settings


NEWS = 'news'


@pytest.mark.django_db
def test_news_in_list_for_author(news_list, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(news_list, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(comments_list, news, client):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert NEWS in response.context
    news = response.context[NEWS]
    all_timestamps = sorted([
        comment.created for comment in news.comment_set.all()]
    )
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(news, client):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.parametrize(
    'parametrized_client, bool_status',
    (
        (lazy_fixture('client'), False),
        (lazy_fixture('author_client'), True)
    )
)
@pytest.mark.django_db
def test_authorized_client_has_form(news, parametrized_client, bool_status):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    assert bool('form' in response.context) is bool_status
