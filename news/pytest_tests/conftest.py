"""Тесты маршрутов."""
import pytest
from django.utils import timezone
from datetime import datetime, timedelta

from django.test.client import Client

from django.conf import settings
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    """Модели пользователей."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Не автор новости, но авторизованный пользователь."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Авторизация автора новости."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Авторизация пользователя."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    """Новость автора."""
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def comment(news, author):
    """Комментарий к новости автора."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария автора.'
    )
    return comment


@pytest.fixture
def other_comment(news, not_author):
    """Комментарий к новости не автора."""
    comment = Comment.objects.create(
        news=news,
        author=not_author,
        text='Текст комментария не автора.'
    )
    return comment


@pytest.fixture
def many_news():
    """Создание новостей на несколько страниц."""
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            # Для каждой новости уменьшаем дату на index дней от today,
            # где index - счётчик цикла.
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 11)
    ]
    return News.objects.bulk_create(all_news)
