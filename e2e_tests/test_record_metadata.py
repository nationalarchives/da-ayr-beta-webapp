import re

from playwright.sync_api import Page, expect


def test_page_title_and_header(aau_user_page: Page):
    """
    Given the user accesses AYR
    When the user loads the record page
    Then the AYR record title should be displayed
    """
    aau_user_page.goto("/record")
    expect(aau_user_page).to_have_title(
        re.compile("Page not found – AYR - Access Your Records – GOV.UK")
    )
    expect(aau_user_page.get_by_text("Page not found")).to_be_visible()


def test_invalid_record(aau_user_page: Page):
    """
    Given the user accesses AYR
    When the user loads an invalid record page
    Then the AYR 404 page should be displayed
    """
    aau_user_page.goto("/record")
    expect(aau_user_page.get_by_text("Page not found")).to_be_visible()


def test_back_link(aau_user_page: Page):
    """
    Given a user is on the record page
    When the user selects the back button / breadcrumb
    Then the user should be navigated back to the results page
    """
    aau_user_page.goto("/search")
    aau_user_page.locator("#search-input").click()
    aau_user_page.locator("#search-input").fill("pptx")
    aau_user_page.get_by_role("button", name="Search").click()
    expect(aau_user_page.get_by_text("record(s) found")).to_be_visible()
    aau_user_page.get_by_role("link", name="Presentation.pptx").first.click()
    aau_user_page.get_by_role("link", name="Back", exact=True).click()
    aau_user_page.wait_for_url("/search")
    aau_user_page.close()


def test_searched_record_metadata(aau_user_page: Page):
    """
    Given the user has clicked on a result displayed on the search page with results displayed.
    When the user is on the record page
    Then the table should display the relevant metadata for the record such as
        "File name"
    """
    aau_user_page.goto("/search")
    aau_user_page.locator("#search-input").click()
    aau_user_page.locator("#search-input").fill("pptx")
    aau_user_page.get_by_role("button", name="Search").click()
    expect(aau_user_page.get_by_text("record(s) found")).to_be_visible()
    aau_user_page.get_by_role("link", name="Presentation.pptx").first.click()

    # Verify if the expected metadata is visible on the record page
    assert aau_user_page.locator("dt:has-text('File name') + dd").is_visible()

    # Close the page
    aau_user_page.close()
