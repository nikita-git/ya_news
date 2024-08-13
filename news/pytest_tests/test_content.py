"""Тест контента."""
# - Комментарии на странице отдельной новости отсортированы в
# хронологическом порядке: старые в начале списка, новые — в конце.
# - Анонимному пользователю недоступна форма для отправки комментария
# на странице отдельной новости, а авторизованному доступна.
import pytest
from pytest_django.asserts import assertInHTML

from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_news_count(many_news, client):
    """Тест количества новостей на странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(many_news, client):
    """Тест сортировки новостей."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(news, client):
    """Тест сортировки комментариев."""
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    # Проверяем, что объект новости находится в словаре контекста
    # под ожидаемым именем - названием модели.
    assert 'news' in response.context
    # Получаем объект новости.
    news = response.context['news']
    # Получаем все комментарии к новости.
    all_comments = news.comment_set.all()
    print(f'{all_comments}')
    # Собираем временные метки всех новостей.
    all_timestamps = [comment.created for comment in all_comments]
    # Сортируем временные метки, менять порядок сортировки не надо.
    sorted_timestamps = sorted(all_timestamps)
    # Проверяем, что временные метки отсортированы правильно.
    assert all_timestamps == sorted_timestamps
