"""Тесты логики."""
from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertFormError
from news.models import Comment
from news.forms import BAD_WORDS, WARNING

@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=('1',))
    count_comment_now = Comment.objects.count()
    client.post(url, data={'text': 'ANONYMOUS'})
    assert Comment.objects.count() == count_comment_now


@pytest.mark.parametrize(
   'parameter_client',
   (
        pytest.lazy_fixture('author_client'),
        pytest.lazy_fixture('not_author_client')
   ),
)
@pytest.mark.parametrize(
    'name, args, count_comment',
    (
        ('news:detail', '1', 3),
        ('news:edit', '1', 2),
    ), 
)
def test_user_can_create_edit_comment(
    parameter_client,
    name,
    args,
    count_comment,
    news,
    comment,
    other_comment
):
    """Пользователи могут создавать и редактировать комментарии."""
    url = reverse(name, args=(args,))
    parameter_client.post(url, data={'text': 'Comment'})
    assert Comment.objects.count() == count_comment


def test_author_can_delete_comment(
    author_client,
    news,
    comment
):
    """Удаления комментариев автором."""
    url = reverse('news:delete', args=(news.id,))
    count_comment = Comment.objects.count()
    author_client.post(url)
    assert Comment.objects.count() < count_comment


def test_other_author_can_delete_comment(
    not_author_client,
    news,
    other_comment
):
    """Удаления комментариев автором."""
    url = reverse('news:delete', args=(news.id,))
    count_comment = Comment.objects.count()
    not_author_client.post(url)
    assert Comment.objects.count() < count_comment


def test_other_user_cant_delete_note(not_author_client, news, comment):
    """Авторизованный пользователь не может удалить чужой комментарий."""
    url = reverse('news:delete', args=(news.id,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, news):
    """Тест на содержание запрещенных слов."""
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_data)
    print(f'{response}')
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0
