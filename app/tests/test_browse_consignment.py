import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from app.tests.assertions import assert_contains_html
from app.tests.test_browse import verify_data_rows


def verify_consignment_view_header_row(data):
    """
    this function check header row column values against expected row
    :param data: response data
    """
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table")
    headers = table.find_all("th")
    expected_row = (
        [
            "Record date",
            "Filename",
            "Status",
            "Record opening date",
        ],
    )
    assert [
        header.text.replace("\n", " ").strip(" ") for header in headers
    ] == expected_row[0]


class TestConsignment:
    @property
    def route_url(self):
        return "/browse/consignment"

    @property
    def transferring_body_route_url(self):
        return "/browse/transferring_body"

    @property
    def series_route_url(self):
        return "/browse/series"

    def test_browse_consignment_breadcrumb(
        self,
        client: FlaskClient,
        mock_standard_user,
        browse_consignment_files,
    ):
        """
        Given a user accessing the browse page
        When they make a GET request with a consignment id
        Then they should see results based on consignment filter on browse page content.
        And breadcrumb should show 'Everything' > transferring body name > series name > consignment reference
        """
        consignment_id = browse_consignment_files[0].consignment.ConsignmentId

        mock_standard_user(
            client, browse_consignment_files[0].consignment.series.body.Name
        )

        response = client.get(f"{self.route_url}/{consignment_id}")

        assert response.status_code == 200
        assert b"You are viewing" in response.data

        html = response.data.decode()
        consignment_reference = browse_consignment_files[
            0
        ].consignment.ConsignmentReference
        expected_breadcrumbs_html = f"""
        <div class="govuk-breadcrumbs">
            <ol class="govuk-breadcrumbs__list">
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link--record" href="/browse">Everything</a>
                </li>
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link--record--transferring-body"
                        href="{self.transferring_body_route_url}/{browse_consignment_files[0].consignment.series.body.BodyId}">{browse_consignment_files[0].consignment.series.body.Name}</a>
                </li>
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link--record--series"
                        href="{self.series_route_url}/{browse_consignment_files[0].consignment.series.SeriesId}">{browse_consignment_files[0].consignment.series.Name}</a>
                </li>
                <li class="govuk-breadcrumbs__list-item">
                    <span class="govuk-breadcrumbs__link govuk-breadcrumbs__link--record">{consignment_reference}</span>
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

    @pytest.mark.parametrize(
        "query_params, expected_results",
        [
            (
                "date_filter_field=date_last_modified&date_from_day=01&date_from_month=05&date_from_year=2024",
                [
                    [""],
                ],
            ),
            (
                "",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "date_from_day=01&date_from_month=01&date_from_year=2020",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "date_to_day=10&date_to_month=03&date_to_year=2023",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "date_from_day=01&date_from_month=01&date_from_year=2020&date_to_day=10"
                "&date_to_month=03&date_to_year=2023",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "sort=closure_type-asc",
                [
                    [
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=date_last_modified-desc",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-'"
                    ],
                ],
            ),
            (
                "sort=date_last_modified-asc",
                [
                    [
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-'"
                    ],
                ],
            ),
            (
                "sort=file_name-asc",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=file_name-desc",
                [
                    [
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all&date_filter_field=date_last_modified"
                "&date_from_day=01&date_from_month=01&date_from_year=2020&date_to_day=10"
                "&date_to_month=03&date_to_year=2023",
                [
                    [
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all&date_filter_field=date_last_modified"
                "&date_from_day=01&date_from_month=01&date_from_year=2020",
                [
                    [
                        "'20/05/2023', 'fifth_file.doc', 'Open', '-', "
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all&date_filter_field=date_last_modified"
                "&date_to_day=10&date_to_month=03&date_to_year=2023",
                [
                    [
                        "'15/01/2023', 'second_file.ppt', 'Open', '-', "
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all&date_filter_field=opening_date"
                "&date_from_day=01&date_from_month=01&date_from_year=2023",
                [
                    [
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=opening_date-asc&record_status=all&date_filter_field=opening_date"
                "&date_to_day=03&date_to_month=04&date_to_year=2023",
                [
                    [
                        "'25/02/2023', 'first_file.docx', 'Closed', '25/02/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
            (
                "sort=closure_type-desc&record_status=all&date_filter_field=opening_date"
                "&date_from_day=10&date_from_month=03&date_from_year=2023&date_to_day=20"
                "&date_to_month=10&date_to_year=2023",
                [
                    [
                        "'12/04/2023', 'fourth_file.xls', 'Closed', '12/04/2023', "
                        "'10/03/2023', 'third_file.docx', 'Closed', '10/03/2023'"
                    ],
                ],
            ),
        ],
    )
    def test_browse_consignment_full_test(
        self,
        client: FlaskClient,
        mock_standard_user,
        browse_consignment_files,
        query_params,
        expected_results,
    ):
        """
        Given a standard user accessing the browse page
        When they make a GET request with a consignment id
        and provide different filter values
        and sorting orders (asc, desc)
        Then they should see results based on consignment and
        matches to filter value(s) and the result sorted in sorting order
        on browse page content.
        """
        mock_standard_user(
            client, browse_consignment_files[0].consignment.series.body.Name
        )

        consignment_id = browse_consignment_files[0].consignment.ConsignmentId

        response = client.get(
            f"{self.route_url}/{consignment_id}?{query_params}"
        )

        assert response.status_code == 200

        verify_consignment_view_header_row(response.data)
        verify_data_rows(response.data, expected_results)