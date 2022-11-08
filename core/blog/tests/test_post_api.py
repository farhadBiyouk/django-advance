import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime


@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_post_response_200_status(self):

        url = reverse('blog:api-v1:post-list')
        response = self.client.get(url)

        assert response.status_code == 200

    def test_create_post_response_401_status(self):
        url = reverse('blog:api-v1:post-list')
        data = {
            "title": 'test for pytest',
            "content": 'description for pytest',
            "published_date": datetime.now(),
            "status": True,
        }
        response = self.client.post(url, data)

        assert response.status_code == 401
