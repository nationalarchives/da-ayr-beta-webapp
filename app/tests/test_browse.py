from bs4 import BeautifulSoup
from flask import url_for
from flask.testing import FlaskClient

from app.tests.assertions import assert_contains_html
from app.tests.factories import BodyFactory
from app.tests.mock_database import (
    create_multiple_files_for_consignment,
    create_multiple_test_records,
)


def test_standard_user_redirected_to_browse_transferring_body_when_accessing_browse(
    client: FlaskClient, mock_standard_user
):
    """
    Given a standard user accessing the browse page
    When they make a GET request
    Then they should be redirected to the transferring_body browse page for
        the body they have access to
    """
    body = BodyFactory()
    mock_standard_user(client, body.Name)

    response = client.get("/browse")

    assert response.status_code == 302
    assert response.headers["Location"] == url_for(
        "main.browse", transferring_body_id=body.BodyId
    )


def test_browse_get(client: FlaskClient, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a GET request
    Then they should see the browse page content.
    """
    mock_superuser(client)

    response = client.get("/browse")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data


def test_browse_submit_search_query(client: FlaskClient, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a POST request
    Then they should see results in content.
    """
    mock_superuser(client)
    create_multiple_test_records()

    query = "test"
    response = client.post("/browse", data={"query": query})

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"Records found 11" in response.data


def test_browse_get_with_data(client: FlaskClient, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a GET request with page as a query string parameter
    Then they should see first five records on browse page content.
    """
    mock_superuser(client)
    create_multiple_test_records()

    response = client.get("/browse")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        [
            "'test body1', 'test series1', '01/01/2023', '1', '1', "
            "'test body2', 'test series2', '01/01/2023', '1', '1', "
            "'testing body10', 'test series10', '01/01/2023', '1', '1', "
            "'testing body11', 'test series11', '01/01/2023', '2', '1', "
            "'testing body3', 'test series3', '01/01/2023', '1', '1'"
        ],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]


def test_browse_display_first_page(client: FlaskClient, app, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a GET request with page as a query string parameter
    Then they should see first page with five records on browse page content
    (excluding previous and incl. next page option).
    """
    mock_superuser(client)
    create_multiple_test_records()
    app.config["DEFAULT_PAGE_SIZE"] = 5

    response = client.get("/browse?page=1")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data
    assert b'aria-label="Page 1"' in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")
    previous_option = soup.find("div", {"class": "govuk-pagination__prev"})
    next_option = soup.find("div", {"class": "govuk-pagination__next"})

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        [
            "'test body1', 'test series1', '01/01/2023', '1', '1', "
            "'test body2', 'test series2', '01/01/2023', '1', '1', "
            "'testing body10', 'test series10', '01/01/2023', '1', '1', "
            "'testing body11', 'test series11', '01/01/2023', '2', '1', "
            "'testing body3', 'test series3', '01/01/2023', '1', '1'"
        ],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]
    assert not previous_option
    assert next_option.text.replace("\n", "").strip("") == "Nextpage"


def test_browse_display_middle_page(client: FlaskClient, app, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a GET request with page as a query string parameter
    Then they should see first page with five records on browse page content (incl. previous and next page options).
    """
    mock_superuser(client)
    create_multiple_test_records()
    app.config["DEFAULT_PAGE_SIZE"] = 5

    response = client.get("/browse?page=2")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data
    assert b'aria-label="Page 2"' in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")
    page_options = soup.find_all("span", class_="govuk-pagination__link-title")

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        [
            "'testing body4', 'test series4', '01/01/2023', '1', '1', "
            "'testing body5', 'test series5', '15/02/2023', '1', '1', "
            "'testing body6', 'test series6', '15/02/2023', '1', '1', "
            "'testing body7', 'test series7', '15/02/2023', '1', '1', "
            "'testing body8', 'test series8', '15/02/2023', '1', '1'"
        ],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]
    assert (
        " ".join(page_options[0].text.replace("\n", "").split())
        == "Previouspage"
    )
    assert (
        " ".join(page_options[1].text.replace("\n", "").split()) == "Nextpage"
    )


def test_browse_display_last_page(client: FlaskClient, app, mock_superuser):
    """
    Given a superuser accessing the browse page
    When they make a GET request with page as a query string parameter
    Then they should see last page with n records on browse page content
    (incl. previous and excluding next page option).
    """
    mock_superuser(client)
    create_multiple_test_records()
    app.config["DEFAULT_PAGE_SIZE"] = 5

    response = client.get("/browse?page=3")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data
    assert b'aria-label="Page 3"' in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")
    previous_option = soup.find("div", {"class": "govuk-pagination__prev"})
    next_option = soup.find("div", {"class": "govuk-pagination__next"})

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        ["'testing body9', 'test series9', '15/02/2023', '1', '1'"],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]
    assert (
        " ".join(previous_option.text.replace("\n", "").split())
        == "Previouspage"
    )
    assert not next_option


def test_browse_display_multiple_pages(
    client: FlaskClient, app, mock_superuser
):
    """
    Given a superuser accessing the browse page
    When they make a GET request with page as a query string parameter
    Then they should see first page with five records on browse page content (incl. previous and next page options).
    """
    mock_superuser(client)
    create_multiple_test_records()
    app.config["DEFAULT_PAGE_SIZE"] = 5

    response = client.get("/browse?page=1")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Everything available to you" in response.data
    assert b'aria-label="Page 1"' in response.data
    assert b'aria-label="Page 2"' in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")
    # page_options = soup.find_all("span", class_="govuk-pagination__link-title")
    previous_option = soup.find("div", {"class": "govuk-pagination__prev"})
    next_option = soup.find("div", {"class": "govuk-pagination__next"})
    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        [
            "'test body1', 'test series1', '01/01/2023', '1', '1', "
            "'test body2', 'test series2', '01/01/2023', '1', '1', "
            "'testing body10', 'test series10', '01/01/2023', '1', '1', "
            "'testing body11', 'test series11', '01/01/2023', '2', '1', "
            "'testing body3', 'test series3', '01/01/2023', '1', '1'"
        ],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]
    assert not previous_option
    assert next_option.text.replace("\n", "").strip("") == "Nextpage"


def test_browse_transferring_body(client: FlaskClient, mock_standard_user):
    """
    Given a user accessing the browse page
    When they make a GET request with a transferring body id
    Then they should see results based on transferring body filter on browse page content.
    """
    files = create_multiple_test_records()
    file = files[0]
    transferring_body_id = file.consignment.series.body.BodyId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(
        f"/browse?transferring_body_id={transferring_body_id}"
    )

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"test body1" in response.data
    assert b"Records found 1" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Last record transferred",
            "Records held",
            "Consignments within series",
        ],
        ["'test body1', 'test series1', '01/01/2023', '1', '1'"],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]


def test_browse_transferring_body_breadcrumb(
    client: FlaskClient, mock_standard_user
):
    """
    Given a user accessing the browse page
    When they make a GET request with a transferring body id
    Then they should see results based on transferring body filter on browse page content.
    And breadcrumb should show 'Everything' > transferring body name
    """
    files = create_multiple_test_records()
    file = files[0]
    transferring_body_id = file.consignment.series.body.BodyId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(
        f"/browse?transferring_body_id={transferring_body_id}"
    )

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Records found 1" in response.data

    html = response.data.decode()

    expected_breadcrumbs_html = f"""
    <div class="govuk-breadcrumbs">
        <ol class="govuk-breadcrumbs__list">
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record" href="/browse">Everything</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
            <p class="govuk-breadcrumbs__link--record">{file.consignment.series.body.Name}</p>
            </li>
        </ol>
    </div>
    """

    assert_contains_html(
        expected_breadcrumbs_html,
        html,
        "div",
        {"class": "govuk-breadcrumbs"},
    )


def test_browse_series(client: FlaskClient, mock_standard_user):
    """
    Given a user accessing the browse page
    When they make a GET request with a series id
    Then they should see results based on series filter on browse page content.
    """
    files = create_multiple_test_records()
    file = files[0]
    series_id = file.consignment.SeriesId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?series_id={series_id}")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"test body1" in response.data
    assert b"test series1" in response.data
    assert b"Records found 1" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("td")

    expected_results_table = [
        [
            "Transferring body",
            "Series",
            "Consignment transferred",
            "Records in consignment",
            "Consignment reference",
        ],
        [
            "'test body1', 'test series1', '01/01/2023', '1', 'test consignment1'"
        ],
    ]

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]
    row_data = ""
    for row_index, row in enumerate(rows):
        row_data = row_data + "'" + row.text.replace("\n", " ").strip(" ") + "'"
        if row_index < len(rows) - 1:
            row_data = row_data + ", "
    assert [row_data] == expected_results_table[1]


def test_browse_series_breadcrumb(client: FlaskClient, mock_standard_user):
    """
    Given a user accessing the browse page
    When they make a GET request with a series id
    Then they should see results based on series filter on browse page content.
    And breadcrumb should show 'Everything' > transferring body name > series name
    """
    files = create_multiple_test_records()
    file = files[0]
    series_id = file.consignment.SeriesId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?series_id={series_id}")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"Records found 1" in response.data

    html = response.data.decode()

    expected_breadcrumbs_html = f"""
    <div class="govuk-breadcrumbs">
        <ol class="govuk-breadcrumbs__list">
            <li class="govuk-breadcrumbs__list-item">
                <a class="govuk-breadcrumbs__link--record" href="/browse">Everything</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
                <a class="govuk-breadcrumbs__link--record"
                    href="/browse?transferring_body_id={file.consignment.series.body.BodyId}">{file.consignment.series.body.Name}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
                <p class="govuk-breadcrumbs__link--record">{file.consignment.series.Name}</p>
            </li>
        </ol>
    </div>
    """

    assert_contains_html(
        expected_breadcrumbs_html,
        html,
        "div",
        {"class": "govuk-breadcrumbs"},
    )


def test_browse_consignment(client: FlaskClient, mock_standard_user):
    """
    Given a user accessing the browse page
    When they make a GET request with a consignment id
    Then they should see results based on consignment filter on browse page content.
    """
    files = create_multiple_test_records()
    file = files[0]
    consignment_id = file.consignment.ConsignmentId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?consignment_id={consignment_id}")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"test body1" in response.data
    assert b"test series1" in response.data
    assert b"test consignment1" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("tr")

    expected_results_table = [
        [
            "Last modified",
            "Filename",
            "Status",
            "Closure start date",
            "Closure period",
        ],
        ["15/12/2023", "test_file1.pdf", "open", "-", "-"],
    ]

    assert len(rows) == 2

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]

    for index, row in enumerate(rows[1:]):
        values = row.find_all("td")
        assert [
            value.text.replace("\n", " ").strip(" ") for value in values
        ] == expected_results_table[index + 1]


def test_browse_consignment_breadcrumb(client: FlaskClient, mock_standard_user):
    """
    Given a user accessing the browse page
    When they make a GET request with a consignment id
    Then they should see results based on consignment filter on browse page content.
    And breadcrumb should show 'Everything' > transferring body name > series name > consignment reference
    """
    files = create_multiple_test_records()
    file = files[0]
    consignment_id = file.consignment.ConsignmentId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?consignment_id={consignment_id}")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data

    html = response.data.decode()
    print(html)
    expected_breadcrumbs_html = f"""
    <div class="govuk-breadcrumbs">
        <ol class="govuk-breadcrumbs__list">
            <li class="govuk-breadcrumbs__list-item">
                <a class="govuk-breadcrumbs__link--record" href="/browse">Everything</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
                <a class="govuk-breadcrumbs__link--record"
                    href="/browse?transferring_body_id={file.consignment.series.body.BodyId}">{file.consignment.series.body.Name}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
                <a class="govuk-breadcrumbs__link--record"
                    href="/browse?series_id={file.consignment.series.SeriesId}">{file.consignment.series.Name}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
                <p class="govuk-breadcrumbs__link--record">{file.consignment.ConsignmentReference}</p>
            </li>
        </ol>
    </div>
    """
    print(expected_breadcrumbs_html)
    assert_contains_html(
        expected_breadcrumbs_html,
        html,
        "div",
        {"class": "govuk-breadcrumbs"},
    )


def test_browse_consignment_with_missing_file(
    client: FlaskClient, mock_standard_user
):
    """
    Given a user accessing the browse page
    When they make a GET request with a consignment id
    and if file metadata not available for the corresponding file(s)
    Then they should see results based on consignment filter on browse page content
    (including file_name field and rest of the field values as 'None').
    """
    files = create_multiple_test_records()
    file = files[10]
    consignment_id = file.consignment.ConsignmentId

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?consignment_id={consignment_id}")

    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"testing body11" in response.data
    assert b"test series11" in response.data
    assert b"test consignment11" in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("tr")

    expected_results_table = [
        [
            "Last modified",
            "Filename",
            "Status",
            "Closure start date",
            "Closure period",
        ],
        ["None", "test_file11.txt", "closed", "-", "-"],
        ["None", "test_file12.txt", "None", "-", "-"],
    ]

    assert len(rows) == 3

    headers = [header.text.strip() for header in table.find_all("th")]
    assert headers == expected_results_table[0]

    for index, row in enumerate(rows[1:]):
        values = row.find_all("td")
        assert [
            value.text.replace("\n", " ").strip(" ") for value in values
        ] == expected_results_table[index + 1]


def test_browse_consignment_filter_display_multiple_pages(
    client: FlaskClient, app, mock_standard_user
):
    """
    Given a user accessing the browse page
    When they make a GET request with a consignment id
    Then they should see results based on consignment filter on browse page content.
    """
    app.config["DEFAULT_PAGE_SIZE"] = 5

    files = create_multiple_test_records()
    file = files[0]
    consignment_id = file.consignment.ConsignmentId

    create_multiple_files_for_consignment(consignment_id)

    mock_standard_user(client, file.consignment.series.body.Name)

    response = client.get(f"/browse?page=2&consignment_id={consignment_id}")
    assert response.status_code == 200
    assert b"Search for digital records" in response.data
    assert b"You are viewing" in response.data
    assert b"test body1" in response.data
    assert b"test series1" in response.data
    assert b"test consignment1" in response.data
    assert b"Records found 7" in response.data
    assert b'aria-label="Page 1"' in response.data
    assert b'aria-label="Page 2"' in response.data

    soup = BeautifulSoup(response.data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    rows = table.find_all("tr")
    page_options = soup.find_all("span", class_="govuk-pagination__link-title")

    expected_results_table = [
        [
            "Last modified",
            "Filename",
            "Status",
            "Closure start date",
            "Closure period",
        ],
        ["15/12/2023", "test_file6.txt", "closed", "05/11/2023", "-"],
        ["15/12/2023", "test_file7.png", "closed", "05/11/2023", "-"],
    ]

    assert len(rows) == 3

    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_results_table[0]

    for index, row in enumerate(rows[1:]):
        values = row.find_all("td")
        assert [
            value.text.replace("\n", " ").strip(" ") for value in values
        ] == expected_results_table[index + 1]

    assert (
        " ".join(page_options[0].text.replace("\n", "").split())
        == "Previouspage"
    )
