from http import HTTPStatus

from .constants import ConstantClass


class TestRoutes(ConstantClass):
    def test_pages_availability_for_author(self):
        """Доступность страниц для аутентифицированного автора."""
        for url in self.urls:
            self.assertEqual(
                self.author_client.get(url).status_code,
                HTTPStatus.OK
            )

    def test_pages_availability_for_reader(self):
        """Доступность страниц для другого пользователя."""
        urls_not_found = (
            self.DETAIL_URL,
            self.EDIT_URL,
            self.DELETE_URL,
        )
        for url in self.urls:
            if url in urls_not_found:
                self.assertEqual(
                    self.reader_client.get(url).status_code,
                    HTTPStatus.NOT_FOUND
                )
            else:
                self.assertEqual(
                    self.reader_client.get(url).status_code,
                    HTTPStatus.OK
                )

    def test_pages_availability_for_anonymous_client(self):
        """Доступность страниц для другого анонимного пользователя."""
        urls_ok = (
            self.LOGIN_URL,
            self.LOGOUT_URL,
            self.SIGNUP_URL,
            self.HOME_URL,
        )

        for url in self.urls:
            if url in urls_ok:
                self.assertEqual(
                    self.client.get(url).status_code,
                    HTTPStatus.OK
                )
            else:
                self.assertRedirects(
                    self.client.get(url),
                    f'{self.LOGIN_URL}?next={url}'
                )
