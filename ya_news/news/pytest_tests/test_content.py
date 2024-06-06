from pytest import mark
from django.conf import settings

from news.forms import CommentForm


pytestmark = mark.django_db


def test_news_in_list_for_author(news_list, client, home_url):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(news_list, client, home_url):
    """Сортировка новостей от самой свежей к самой старой."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(comments_list, news, client, detail_url):
    """Комментарии на странице отдельной новости отсортированы."""
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_timestamps = sorted([
        comment.created for comment in news.comment_set.all()]
    )
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, detail_url):
    """Отсутсвие у авторизованного пользователя отправки формы комментария."""
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(author_client, detail_url):
    """Доступность авторизованному пользователю отправка формы комментария."""
    respone = author_client.get(detail_url)
    assert 'form' in respone.context
    assert isinstance(
        respone.context['form'],
        CommentForm
    )
