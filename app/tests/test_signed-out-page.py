def test_signed_out_page(client):
    response = client.get("/signed-out")

    assert response.status_code == 200
    assert (
        b'<h1 class="govuk-heading-l">You have successfully signed out</h1>'
        in response.data
    )
    assert (
        b'<p class="govuk-body-l">Thank you for using Access Your Records.</p>'
        in response.data
    )

    assert (
        b'<a href="/login" role="button" class="govuk-button govuk-button--sign-in-again" '
        b'data-module="govuk-button">Sign back in'
    ) in response.data
