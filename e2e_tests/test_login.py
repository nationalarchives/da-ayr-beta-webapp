import json
import zlib

import jwt
from itsdangerous import base64_decode
from playwright.sync_api import Page, expect


def test_sign_in_succeeds_when_valid_credentials(
    page: Page, create_aau_keycloak_user
):
    """
    Given a user is on the sign-in page,
    When they provide valid credentials and click the "Sign in" button,
    Then they should see a success message indicating they are logged in with access to AYR.
    And they should be on the '/browse' page.
    """
    username, password = create_aau_keycloak_user
    page.goto("/sign-in")
    page.get_by_label("Email address").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    expect(page).to_have_url("/browse")

    cookies = page.context.cookies()
    for index, cookie in enumerate(cookies):
        if cookie["name"] == "session":
            session_cookie_index = index
            break

    flask_session_cookie = cookies[session_cookie_index]
    flask_session_cookie_string = flask_session_cookie["value"]

    decoded_data = decode_flask_session_cookie(flask_session_cookie_string)
    access_token = json.loads(decoded_data)["access_token"]
    decoded_token_dict = jwt.decode(
        access_token, options={"verify_signature": False}
    )
    assert set(decoded_token_dict.keys()) == {
        "aud",
        "exp",
        "iat",
        "auth_time",
        "jti",
        "realm_access",
        "resource_access",
        "iss",
        "sub",
        "typ",
        "azp",
        "scope",
        "sid",
        "groups",
    }

    refresh_token = json.loads(decoded_data)["refresh_token"]
    decoded_token_dict = jwt.decode(
        refresh_token, options={"verify_signature": False}
    )
    assert set(decoded_token_dict.keys()) == {
        "aud",
        "exp",
        "iat",
        "jti",
        "iss",
        "sub",
        "typ",
        "azp",
        "scope",
        "sid",
    }


def test_token_expiry(page: Page, create_aau_keycloak_user):
    """
    Given a user is signed in,
    When their refresh token is retrieved,
    Then it should contain expected claims and have an expiry time matching Keycloak config.
    """
    username, password = create_aau_keycloak_user

    page.goto("/sign-in")
    page.get_by_label("Email address").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    expect(page).to_have_url("/browse")

    cookies = page.context.cookies()
    for index, cookie in enumerate(cookies):
        if cookie["name"] == "session":
            session_cookie_index = index
            break

    flask_session_cookie = cookies[session_cookie_index]
    flask_session_cookie_string = flask_session_cookie["value"]
    decoded_data = decode_flask_session_cookie(flask_session_cookie_string)

    access_token = json.loads(decoded_data)["access_token"]
    decoded_access_token = jwt.decode(
        access_token, options={"verify_signature": False}
    )
    exp_time = decoded_access_token["exp"]
    iat_time = decoded_access_token["iat"]
    token_lifetime = exp_time - iat_time
    expected_lifetime = 300

    assert (
        abs(token_lifetime - expected_lifetime) < 5
    ), "Access token expiry does not match expected config"

    refresh_token = json.loads(decoded_data)["refresh_token"]
    decoded_refresh_token = jwt.decode(
        refresh_token, options={"verify_signature": False}
    )
    exp_time = decoded_refresh_token["exp"]
    iat_time = decoded_refresh_token["iat"]
    token_lifetime = exp_time - iat_time
    expected_lifetime = 7200
    assert (
        abs(token_lifetime - expected_lifetime) < 5
    ), "Refresh token expiry does not match expected config"


def decode_flask_session_cookie(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith("."):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(
            e
        )


def test_sign_in_fails_when_invalid_credentials(page: Page):
    """
    Given a user is on the sign-in page,
    When they provide invalid credentials and click the "Sign in" button,
    Then they should see an error message indicating the provided credentials are invalid.
    """
    page.goto("/sign-in")
    page.get_by_label("Email address").fill("bad")
    page.get_by_label("Password").fill("credentials")
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Invalid username or password."))
