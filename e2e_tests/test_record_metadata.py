import re

from playwright.sync_api import Page, expect


def test_page_title_and_header(authenticated_page: Page):
    """
    Given the user accesses AYR
    When the user loads the record page
    Then the AYR record title should be displayed
    """
    authenticated_page.goto("/record")
    expect(authenticated_page).to_have_title(
        re.compile("Page not found – AYR - Access Your Records – GOV.UK")
    )
    expect(authenticated_page.get_by_text("Page not found")).to_be_visible()


def test_invalid_record(authenticated_page: Page):
    """
    Given the user accesses AYR
    When the user loads an invalid record page
    Then the AYR 404 page should be displayed
    """
    authenticated_page.goto("/record")
    expect(authenticated_page.get_by_text("Page not found")).to_be_visible()


def test_back_link(authenticated_page: Page):
    """
    Given a user is on the record page
    When the user selects the back button / breadcrumb
    Then the user should be navigated back to the the results page
    """
    authenticated_page.goto("/poc-search-view")
    authenticated_page.locator("#searchInput").click()
    authenticated_page.locator("#searchInput").fill("public record")
    authenticated_page.get_by_role("button", name="Search").click()
    expect(authenticated_page.get_by_text("records found")).to_be_visible()
    authenticated_page.get_by_role("link", name="file-b2.txt").click()
    authenticated_page.get_by_role("link", name="Back", exact=True).click()
    authenticated_page.wait_for_url("/poc-search-view")
    authenticated_page.close()


def test_searched_record_metadata(authenticated_page: Page):
    """
    Given the user has clicked on a result displayed on the search page with results displayed.
    When the user is on the record page
    Then the table should display the relevant metadata for the record such as
        "Source organisation" and "Consignment ID,"
    """
    authenticated_page.goto("/poc-search-view")
    authenticated_page.locator("#searchInput").click()
    authenticated_page.locator("#searchInput").fill("public record")
    authenticated_page.get_by_role("button", name="Search").click()
    expect(authenticated_page.get_by_text("records found")).to_be_visible()
    authenticated_page.get_by_role("link", name="file-b2.txt").click()

    # Verify if the expected metadata is visible on the record page
    assert authenticated_page.locator(
        "dt:has-text('Source organisation') + dd"
    ).is_visible()
    assert authenticated_page.locator(
        "dt:has-text('Consignment ID') + dd"
    ).is_visible()

    # Close the page
    authenticated_page.close()
