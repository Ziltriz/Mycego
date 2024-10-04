import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from .views import IndexView

@pytest.fixture
def client():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    return client

@pytest.fixture
def public_key():
    return 'your_public_key_here'

@pytest.fixture
def filter():
    return 'image'

def test_index_view(client, public_key, filter):
    url = reverse('index')
    response = client.post(url, {'public_key': public_key, 'filter': filter})
    assert response.status_code == 200
    assert 'files' in response.context
    assert 'public_key' in response.context
    assert 'filters' in response.context

def test_index_view_without_filter(client, public_key):
    url = reverse('index')
    response = client.post(url, {'public_key': public_key})
    assert response.status_code == 200
    assert 'files' in response.context
    assert 'public_key' in response.context
    assert 'filters' in response.context

def test_index_view_invalid_public_key(client, public_key):
    url = reverse('index')
    invalid_public_key = 'invalid_public_key'
    response = client.post(url, {'public_key': invalid_public_key})
    assert response.status_code == 200
    assert 'files' not in response.context
    assert 'public_key' in response.context
    assert 'filters' in response.context

def test_index_view_invalid_filter(client, public_key):
    url = reverse('index')
    invalid_filter = 'invalid_filter'
    response = client.post(url, {'public_key': public_key, 'filter': invalid_filter})
    assert response.status_code == 200
    assert 'files' not in response.context
    assert 'public_key' in response.context
    assert 'filters' in response.contextfrom

