from playwright.sync_api import Page


def verify_header_row(header_rows):
    assert header_rows[0] == [
        "Transferring body",
        "Series",
        "Last consignment transferred",
        "Records held in series",
        "Consignments within series",
    ]


class TestBrowseTransferringBody:
    @property
    def route_url(self):
        return "/browse/transferring_body"

    @property
    def transferring_body_id(self):
        return "c969a99f-dd61-4890-a8b4-6556d5d69915"

    def test_browse_transferring_body_has_title(self, standard_user_page: Page):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")

        assert (
            standard_user_page.title()
            == "Browse – AYR - Access Your Records – GOV.UK"
        )

    def test_browse_transferring_body_404_for_no_access(
        self, standard_user_page: Page
    ):
        transferring_body_id = "6b63aa4d-7838-4010-b6f8-66fb3c07823d"

        standard_user_page.goto(f"{self.route_url}/{transferring_body_id}")
        assert standard_user_page.inner_html("text='Page not found'")
        assert standard_user_page.inner_html(
            "text='If you typed the web address, check it is correct.'"
        )
        assert standard_user_page.inner_html(
            "text='If you pasted the web address, check you copied the entire address.'"
        )

    def test_browse_transferring_body_no_results_found(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#series_filter").click()
        standard_user_page.locator("#series_filter").fill("junk")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        assert standard_user_page.inner_html("text='No results found'")
        assert standard_user_page.inner_html("text='Help with your search'")
        assert standard_user_page.inner_html(
            "text='Try changing or removing one or more applied filters.'"
        )
        assert standard_user_page.inner_html(
            "text='Alternatively, use the breadcrumbs to navigate back to the browse view.'"
        )

    def test_browse_transferring_body_breadcrumb(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")

        assert standard_user_page.inner_html("text='You are viewing'")
        assert standard_user_page.inner_html("text='Everything'")
        assert standard_user_page.inner_html("text='Testing A'")

    def test_browse_transferring_body_no_pagination(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")

        standard_user_page.locator("#date_to_day").fill("31")
        standard_user_page.locator("#date_to_month").fill("12")
        standard_user_page.locator("#date_to_year").fill("2022")

        standard_user_page.get_by_role("button", name="Apply filters").click()

        assert not standard_user_page.get_by_label("Page 1").is_visible()
        assert not standard_user_page.get_by_label("Page 2").is_visible()
        assert not standard_user_page.get_by_role(
            "link", name="Nextpage"
        ).is_visible()

    def test_browse_transferring_body_filter_functionality_with_query_string_parameters(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(
            f"{self.route_url}/{self.transferring_body_id}?series_filter=&date_from_day01=&"
            f"date_from_month=01&date_from_year=2024&date_to_day=&date_to_month=&date_to_year="
        )

        header_rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        assert len(rows) == 1

        expected_rows = [
            ["Testing A", "TSTA 1", "25/01/2024", "73", "7"],
        ]

        verify_header_row(header_rows)
        assert rows == expected_rows

    def test_browse_transferring_body_sort_functionality_by_series_descending(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.get_by_label("Sort by").select_option("series-desc")
        standard_user_page.get_by_role(
            "button", name="Apply", exact=True
        ).click()

        header_rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        assert len(rows) == 1

        expected_rows = [
            ["Testing A", "TSTA 1", "25/01/2024", "73", "7"],
        ]

        verify_header_row(header_rows)
        assert rows == expected_rows

    def test_browse_transferring_body_filter_functionality_with_series_filter(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#series_filter").fill("TSTA 1")
        standard_user_page.get_by_role("button", name="Apply filters").click()
        standard_user_page.get_by_role(
            "button", name="Apply", exact=True
        ).click()

        header_rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        assert len(rows) == 1

        expected_rows = [
            ["Testing A", "TSTA 1", "25/01/2024", "73", "7"],
        ]

        verify_header_row(header_rows)
        assert rows == expected_rows

    def test_browse_transferring_body_filter_functionality_with_series_filter_wildcard_character(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#series_filter").fill("1")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        header_rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        assert len(rows) == 1

        expected_rows = [
            ["Testing A", "TSTA 1", "25/01/2024", "73", "7"],
        ]

        verify_header_row(header_rows)
        assert rows == expected_rows

    def test_browse_transferring_body_filter_functionality_with_date_filter(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#date_from_day").fill("1")
        standard_user_page.locator("#date_from_month").fill("1")
        standard_user_page.locator("#date_from_year").fill("2024")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        header_rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(0).map(el =>
              [...el.querySelectorAll('th')].map(e => e.textContent.trim())
            )"""
        )

        rows = standard_user_page.locator(
            "#tbl_result tr:visible"
        ).evaluate_all(
            """els => els.slice(1).map(el =>
              [...el.querySelectorAll('td')].map(e => e.textContent.trim())
            )"""
        )

        assert len(rows) == 1

        expected_rows = [
            ["Testing A", "TSTA 1", "25/01/2024", "73", "7"],
        ]

        verify_header_row(header_rows)
        assert rows == expected_rows

    def test_browse_transferring_body_date_filter_validation_date_from(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#date_from_day").fill("1")
        standard_user_page.locator("#date_from_month").fill("12")
        standard_user_page.locator("#date_from_year").fill("2024")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        assert standard_user_page.get_by_text(
            "‘Date from’ must be in the past"
        ).is_visible()

    def test_browse_transferring_body_date_filter_validation_to_date(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#date_to_day").fill("31")
        standard_user_page.locator("#date_to_month").fill("12")
        standard_user_page.locator("#date_to_year").fill("2024")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        assert standard_user_page.get_by_text(
            "‘Date to’ must be in the past"
        ).is_visible()

    def test_browse_transferring_body_date_filter_validation_date_from_and_to_date(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.locator("#date_from_day").fill("1")
        standard_user_page.locator("#date_from_month").fill("1")
        standard_user_page.locator("#date_from_year").fill("2023")
        standard_user_page.locator("#date_to_day").fill("31")
        standard_user_page.locator("#date_to_month").fill("12")
        standard_user_page.locator("#date_to_year").fill("2022")
        standard_user_page.get_by_role("button", name="Apply filters").click()

        assert standard_user_page.get_by_text(
            "‘Date from’ must be the same as or before ‘31/12/2022’"
        ).is_visible()

    def test_browse_transferring_body_clear_filter_functionality(
        self, standard_user_page: Page
    ):
        standard_user_page.goto(f"{self.route_url}/{self.transferring_body_id}")
        standard_user_page.get_by_label("Sort by").select_option("series-desc")
        standard_user_page.get_by_role(
            "button", name="Apply", exact=True
        ).click()
        standard_user_page.get_by_role("link", name="Clear filters").click()
        assert standard_user_page.inner_text("#series_filter") == ""
        assert standard_user_page.inner_text("#date_from_day") == ""
        assert standard_user_page.inner_text("#date_from_month") == ""
        assert standard_user_page.inner_text("#date_from_year") == ""
        assert standard_user_page.inner_text("#date_to_day") == ""
        assert standard_user_page.inner_text("#date_to_month") == ""
        assert standard_user_page.inner_text("#date_to_year") == ""
        assert (
            standard_user_page.get_by_label("Sort by", exact=True).evaluate(
                "el => el.options[el.selectedIndex].text"
            )
            == "Series (Z to A)"
        )
