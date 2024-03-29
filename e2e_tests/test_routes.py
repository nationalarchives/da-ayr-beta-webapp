from playwright.sync_api import Page


class TestRoutes:
    def test_cookies_get(self, standard_user_page: Page):
        standard_user_page.goto("/cookies")

        assert standard_user_page.inner_html("text='Cookies'")
        assert standard_user_page.inner_html("text='Why do we use cookies?'")
        assert standard_user_page.inner_html("text='Essential cookies'")

        header_rows = standard_user_page.locator(
            "#tbl_cookies tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        assert header_rows[0] == [
            "Cookie name",
            "What it does/typical content",
            "Duration",
        ]

        rows = standard_user_page.locator(
            "#tbl_cookies tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        expected_rows = [
            [
                "session",
                "A cookie that holds information for authorisation purpose",
                "Expires when you exit the browser",
            ],
            [
                "KEYCLOAK_SESSION_LEGACY",
                "A cookie set by the authorisation component of the service that keeps track of the session as you "
                "use the service",
                "Expires when you exit the browser",
            ],
            [
                "KEYCLOAK_SESSION",
                "A cookie set by the authorisation component of the service that keeps track of the session as you "
                "use the service",
                "Expires when you exit the browser",
            ],
            [
                "KEYCLOAK_IDENTITY_LEGACY",
                "A cookie set by the authorisation component of the service that keeps track of elements related to "
                "your identity as you use the service",
                "Expires when you exit the browser",
            ],
            [
                "KEYCLOAK_IDENTITY",
                "A cookie set by the authorisation component of the service that keeps track of elements related to "
                "your identity as you use the service",
                "Expires when you exit the browser",
            ],
            [
                "AUTH_SESSION_ID_LEGACY",
                "A cookie set by the authorisation component of the service that keeps track of the session identity "
                "as you use the service",
                "Expires when you exit the browser",
            ],
            [
                "AUTH_SESSION_ID",
                "A cookie set by the authorisation component of the service that keeps track of the session identity "
                "as you use the service",
                "Expires when you exit the browser",
            ],
            [
                "KC_RESTART",
                "A cookie set by the authorisation component of the service that keeps track of the session as you "
                "use the service",
                "Expires when you exit the browser",
            ],
            [
                "KC_AUTH_STATE",
                "A cookie set by the authorisation component of the service that keeps track of the session as you "
                "use the service",
                "Expires when you exit the browser",
            ],
        ]

        assert rows == expected_rows
