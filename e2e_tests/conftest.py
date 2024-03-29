import os

import pytest
from playwright.sync_api import Page


@pytest.fixture()
def aau_user_page(page) -> Page:
    page.goto("/sign-in")
    page.get_by_label("Email address").fill(
        os.environ.get("AYR_AAU_USER_USERNAME")
    )
    page.get_by_label("Password").fill(os.environ.get("AYR_AAU_USER_PASSWORD"))
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("/browse")
    return page


@pytest.fixture()
def standard_user_page(page) -> Page:
    page.goto("/sign-in")
    page.get_by_label("Email address").fill(
        os.environ.get("AYR_STANDARD_USER_USERNAME")
    )
    page.get_by_label("Password").fill(
        os.environ.get("AYR_STANDARD_USER_PASSWORD")
    )
    page.get_by_role("button", name="Sign in").click()
    return page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Fixture for configuring Playwright browser context arguments.
    This fixture is used to customize browser context arguments for Playwright
    browser instances. It sets the 'ignore_https_errors' option to True, which
    allows ignoring HTTPS errors, To disable JS set 'java_script_enabled' to False, which
    disables JavaScript in the browser context.
    Parameters:
        browser_context_args (dict): The default browser context arguments.
    Returns:
        dict: Updated browser context arguments with customized settings.
    """
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "java_script_enabled": False,
    }


@pytest.fixture()
def page(request, page) -> Page:
    page.context.set_default_timeout(5000)
    if "test_css_" not in request.node.name and callable(request.node.obj):

        def route_intercept(route):
            if route.request.resource_type == "stylesheet":
                return route.abort()
            return route.continue_()

        page.route("**/*", route_intercept)
    return page
