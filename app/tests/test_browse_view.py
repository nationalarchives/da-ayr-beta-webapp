from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from app.tests.mock_database import generate_mock_data


def test_browse_view_get(client: FlaskClient):
    """
    Given a user accessing the browse page
    When they make a GET request
    Then they should see the browse page content.
    """
    response = client.get("/poc-browse-view")

    assert response.status_code == 200
    assert b"Browse View" in response.data
    assert b"Everything available to you" in response.data


def test_browse_view_with_no_results(client: FlaskClient):
    """
    Given user logged in application
    When they make a request on the browse page, and no results are found
    Then they should see no records found.
    """

    form_data = {}
    response = client.post("/poc-browse-view", data=form_data)

    assert response.status_code == 200
    assert b"0 record(s) found"


def test_browse_view_results_displayed(client: FlaskClient):
    """
    Given user logged in application
    When they make a request on the browse page
    Then a table is populated with the n results with metadata fields.
    """
    generate_mock_data()

    form_data = {"query": "test"}
    response = client.post("/poc-browse-view", data=form_data)

    assert response.status_code == 200
    assert b"2 record(s) found" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table", class_="govuk-table")
    rows = table.find_all("tr", class_="govuk-table__row")
    header_row = rows[0]
    results_rows = rows[1:]

    headers = header_row.find_all("th")

    expected_results_table = [
        [
            "Transferring Body",
            "Series",
            "Last Record Transferred",
            "Records held",
            "Consignment in Series",
        ],
        ["test body1", "test series1", "2023-01-01 00:00:00", "1", "1"],
        ["test body2", "test series2", "2023-01-01 00:00:00", "1", "1"],
    ]

    assert [header.text for header in headers] == expected_results_table[0]
    for row_index, row in enumerate(results_rows):
        assert [
            result.text for result in row.find_all("td")
        ] == expected_results_table[row_index + 1]
