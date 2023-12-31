from playwright.sync_api import Page


def test_has_title(authenticated_page: Page):
    authenticated_page.goto("/browse")

    assert (
        authenticated_page.title()
        == "Browse – AYR - Access Your Records – GOV.UK"
    )


def test_sort_dropdown(authenticated_page: Page):
    authenticated_page.goto("/browse")
    authenticated_page.select_option("#sort", "body-a")
    authenticated_page.select_option("#sort", "body-b")
    authenticated_page.select_option("#sort", "series-a")
    authenticated_page.select_option("#sort", "series-b")
    authenticated_page.select_option("#sort", "date-first")
    authenticated_page.select_option("#sort", "date-last")


def test_filter_functionality(authenticated_page: Page):
    authenticated_page.goto("/browse")
    authenticated_page.select_option(
        ".govuk-select__filters-form-transferring-body-select",
        "Arts Council England",
    )

    records = authenticated_page.query_selector_all(
        ".govuk-summary-list__value a"
    )
    for record in records:
        assert record
