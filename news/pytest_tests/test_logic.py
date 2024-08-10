"""Тесты логики."""
# Авторизованный пользователь может отправить комментарий.
# Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.
# Авторизованный пользователь может редактировать или удалять свои комментарии.
# Авторизованный пользователь не может редактировать или удалять чужие комментарии.

import pytest
from django.urls import reverse
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=('1',))
    count_comment_now = Comment.objects.count()
    client.post(url, data={'text': 'ANONYMOUS'})
    assert Comment.objects.count() == count_comment_now
