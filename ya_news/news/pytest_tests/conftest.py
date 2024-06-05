from datetime import datetime, timedelta

from _pytest.fixtures import fixture
from django.conf import settings
from django.test.client import Client
from django.urls import reverse


from news.models import Comment, News


@fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author,
    )
    return comment


@fixture
def pk_for_args(news):
    return (news.id,)


@fixture
def news_list():
    today = datetime.today()
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@fixture
def comments_list(author, news):
    for index in range(10):
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )


@fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@fixture
def home_url():
    return reverse('news:home')


@fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@fixture
def login_url():
    return reverse('users:login')


@fixture
def logout_url():
    return reverse('users:logout')


@fixture
def signup_url():
    return reverse('users:signup')
