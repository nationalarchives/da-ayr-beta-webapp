"""
Feature: Record page functionality
"""

from playwright.sync_api import Page


class TestRecord:
    @property
    def route_url(self):
        return "/record"

    def test_record_404_for_no_access(self, standard_user_page: Page):
        """
        Scenario: Accessing a record page without permission results in 404

        Given a standard user with ID of a record in a different transferring body
        When the user navigates to the record page with this ID
        Then the page should display "Page not found"
        """
        record_id = "7ce919c0-9f2b-4133-b41f-f85bdecc6a52"

        standard_user_page.goto(f"{self.route_url}/{record_id}")
        assert standard_user_page.inner_html("text='Page not found'")

    def test_record_metadata_with_open_record_status(
        self, standard_user_page: Page
    ):
        """
        Scenario: Viewing metadata for an open record

        Given the user navigates to the record page with ID of an open record
        Then the fields for open records should be visible
        """
        record_id = "100251bb-5b93-48a9-953f-ad5bd9abfbdc"

        standard_user_page.goto(f"{self.route_url}/{record_id}")
        expected_fields = [
            "File name",
            "Description",
            "Citeable reference",
            "Status",
            "Date of record",
            "Transferring body",
            "Series reference",
            "Consignment reference",
            "File reference",
            "Former reference",
            "Translated file name",
            "Held by",
            "Legal status",
            "Rights copyright",
            "Language",
        ]
        for field in expected_fields:
            assert standard_user_page.get_by_text(
                field, exact=True
            ).is_visible()

    def test_record_metadata_with_closed_record_status(
        self, standard_user_page: Page
    ):
        """
        Scenario: Viewing metadata for a closed record

        Given the user navigates to the record page with ID of a closed record
        Then the fields for closed records should be visible
        """
        record_id = "405ea5a6-b71d-4ecd-be3c-43062af8e1e6"

        standard_user_page.goto(f"{self.route_url}/{record_id}")
        expected_fields = [
            "File name",
            "Alternative file name",
            "Description",
            "Citeable reference",
            "Alternative description",
            "Status",
            "Closure start date",
            "Closure period",
            "Date of record",
            "FOI exemption code(s)",
            "Transferring body",
            "Series reference",
            "Consignment reference",
            "File reference",
            "Former reference",
            "Translated file name",
            "Held by",
            "Legal status",
            "Rights copyright",
            "Language",
        ]

        for field in expected_fields:
            assert standard_user_page.get_by_text(
                field, exact=True
            ).is_visible()

    def test_record_download_record(self, standard_user_page: Page):
        """
        Scenario: Downloading a record

        Given the user navigates to the record page with ID "100251bb-5b93-48a9-953f-ad5bd9abfbdc"
        When the user clicks the "Download record" button
        Then the file "TSTA 1_ZD5B3S.doc" should be downloaded
        """
        record_id = "100251bb-5b93-48a9-953f-ad5bd9abfbdc"
        standard_user_page.goto(f"{self.route_url}/{record_id}")

        with standard_user_page.expect_download() as download_record:
            standard_user_page.get_by_text("Download record").click()
        download = download_record.value
        assert "TSTA 1_ZD5B3S.doc" == download.suggested_filename
