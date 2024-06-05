from http import HTTPStatus

from .constants import ConstantClass


class TestRoutes(ConstantClass):
    """Доступность страниц для аутентифицированного пользователя."""

    def test_pages_availability_for_author(self):
        for url, reader_status, anonymous_status in self.urls:
            with self.subTest(url=url):
                self.assertEqual(
                    self.author_client.get(url).status_code,
                    HTTPStatus.OK
                )

    """Доступность страниц для другого пользователя."""

    def test_pages_availability_for_reader(self):
        for url, reader_status, anonymous_status in self.urls:
            with self.subTest(url=url):
                self.assertEqual(
                    self.reader_client.get(url).status_code,
                    reader_status
                )

    """Доступность страниц для другого анонимного пользователя."""

    def test_pages_availability_for_anonymous_client(self):
        for url, reader_status, anonymous_status in self.urls:
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).status_code,
                    anonymous_status
                )
        for url, reader_status, anonymous_status in self.urls[:6]:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    f'{self.LOGIN_URL}?next={url}'
                )
