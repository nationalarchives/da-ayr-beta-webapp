"""
Feature: Search to record
"""

import re

from playwright.sync_api import Page, expect


def test_search_to_record(aau_user_page: Page):
    """
    Scenario: Navigate from search to a record

    Given the user is on the browse page
    When the user fills the search box with "a"
    And the user clicks the "Search" button
    Then the URL should be "search_results_summary?query=a"
    When the user clicks on the first link in the first cell
    Then the URL should match the pattern "/search/transferring_body/.*"
    When the user clicks on the first link in the third cell
    Then the URL should match the pattern "/record/.*"
    """
    aau_user_page.goto("/browse")

    aau_user_page.get_by_role("textbox").first.fill("a")
    aau_user_page.get_by_role("button", name="Search").click()
    expect(aau_user_page).to_have_url(
        "search_results_summary?query=a&search_area=everywhere"
    )

    aau_user_page.get_by_role("cell").first.get_by_role("link").first.click()
    expect(aau_user_page).to_have_url(
        re.compile(r"\/search\/transferring_body\/.*")
    )

    aau_user_page.get_by_role("cell").nth(2).get_by_role("link").first.click()
    expect(aau_user_page).to_have_url(re.compile(r"\/record\/.*"))
