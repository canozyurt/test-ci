import django
import os
import unittest
from requests import Request

os.environ.setdefault("DJANGO_SETTINGS_MODULE","maasserver.djangosettings.development")
django.setup()

from maasserver.api.domains import DomainsHandler
from maasserver.testing.testcase import MAASServerTestCase


class DomainsHandlerTests(MAASServerTestCase):
    def test_domain_create(self):
        data = {"name": "adfasf"}
        request = Request('POST', 'localhost', data=data)
        request.user = type("User", (), {"is_superuser": True})
        handler = DomainsHandler()
        handler.create(request=request)