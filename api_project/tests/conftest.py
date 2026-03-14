"""Configures tests to use production database."""
import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    from django.conf import settings

    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'http://127.0.0.1:8000/',
        'NAME': 'db',
    }
