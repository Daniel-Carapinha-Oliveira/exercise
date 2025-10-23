import pytest

from django.urls import reverse

from exercise.version import __version__

pytestmark = pytest.mark.django_db


class TestHomepageView:
    def test_view_loads_successfully(self, client):
        response = client.get(reverse('homepage'))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        response = client.get(reverse('homepage'))
        assert 'homepage.html' in [template.name for template in response.templates]

    def test_view_has_correct_context(self, client):
        response = client.get(reverse('homepage'))

        assert 'current_page' in response.context
        assert response.context['current_page'] == 'homepage'

        assert 'version' in response.context
        assert response.context['version'] == __version__
