from django.test import SimpleTestCase
from django.urls import reverse


class IndexViewTestCase(SimpleTestCase):
    def test_index(self):
        url = reverse("index")

        response = self.client.get(path=url, data=None)

        self.assertEqual(response.status_code, 200)
