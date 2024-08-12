"""Тесты маршрутов."""
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import News


@pytest.mark.django_db
def test_empty_db():
    """Доступ к БД."""
    notes_count = News.objects.count()
    assert notes_count == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('users:login', 'users:logout', 'users:signup', 'news:home')
)
def test_home_availability_anonymous(client, name):
    """Проверка доступности страниц анониму."""
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_anonymous(client, news):
    """Проверка доступа к новости анонимом."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args', (('news:edit', '1'), ('news:delete', '1'),)
)
def test_redirect_anonymous(client, name, args):
    """Редирект при попытке отредактировать и удалить комментарий анонимом."""
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parameter_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', '1'),
        ('news:delete', '1')
    ),
)
def test_availability_users(
        parameter_client, name, args, expected_status, comment
):
    """Проверка доступа к комментарию пользователей и автора."""
    url = reverse(name, args=args)
    response = parameter_client.get(url)
    assert response.status_code == expected_status
