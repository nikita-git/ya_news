"""Тест контента."""
# - Новости отсортированы от самой свежей к самой старой.
# Свежие новости в начале списка.
# - Комментарии на странице отдельной новости отсортированы в
# хронологическом порядке: старые в начале списка, новые — в конце.
# - Анонимному пользователю недоступна форма для отправки комментария
# на странице отдельной новости, а авторизованному доступна.
import pytest
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
