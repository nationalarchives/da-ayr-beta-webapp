from typing import List
from unittest.mock import patch

import pytest
from flask.testing import FlaskClient
from testing.postgresql import PostgresqlFactory

from app import create_app
from app.main.db.models import db
from app.tests.factories import (
    BodyFactory,
    ConsignmentFactory,
    FileFactory,
    SeriesFactory,
)
from configs.testing_config import TestingConfig


@pytest.fixture(scope="function")
def mock_standard_user():
    patcher = patch("app.main.authorize.permissions_helpers.get_user_groups")
    mock_get_user_groups = patcher.start()

    def _mock_standard_user(client: FlaskClient, bodies: List[str]):
        with client.session_transaction() as session:
            session["access_token"] = "valid_token"

        groups = [f"/transferring_body_user/{body}" for body in bodies]
        groups.append("/ayr_user_type/view_dept")

        mock_get_user_groups.return_value = groups

    yield _mock_standard_user

    patcher.stop()


@pytest.fixture(scope="function")
def mock_superuser():
    patcher = patch("app.main.authorize.permissions_helpers.get_user_groups")
    mock_get_user_groups = patcher.start()

    def _mock_superuser(client: FlaskClient):
        with client.session_transaction() as session:
            session["access_token"] = "valid_token"

        mock_get_user_groups.return_value = ["/ayr_user_type/view_all"]

    yield _mock_superuser

    patcher.stop()


@pytest.fixture
def app(database):
    app = create_app(TestingConfig, database.url())
    yield app


@pytest.fixture(scope="function")
def client(app):
    db.session.remove()
    db.drop_all()
    db.create_all()
    yield app.test_client()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}


@pytest.fixture(scope="session")
def database(request):
    # Launch new PostgreSQL server
    postgresql = PostgresqlFactory(cache_initialized_db=True)()
    yield postgresql

    # PostgreSQL server is terminated here
    @request.addfinalizer
    def drop_database():
        postgresql.stop()


@pytest.fixture
def browse_files():
    """

    purpose of this function to return file objects to perform testing on
      combination of single and multiple filters
      and single sorting

    returns 28 file objects associated with consignments

    there are 6 bodies defined as Transferring bodies (1 to 5 only have one series),
      body_6 has two series associated with it

    there are 7 series defined as Series (1 to 5 linked directly to one transferring body)
      series_6 and series_7 are linked to one transferring body_6

    there are 12 consignment objects (1 to 12) associated with transferring body and series
      consignment_1 and consignment_2 associated to body_1 and series_1
      consignment_3 and consignment_4 associated to body_2 and series_2
      consignment_5 and consignment_6 associated to body_3 and series_3
      consignment_7 and consignment_8 associated to body_4 and series_4
      consignment_9 and consignment_10 associated to body_5 and series_5
      consignment_11 associated to body_6 and series_6
      consignment_12 associated to body_6 and series_7

      each consignment has a unique ConsignmentReference to support filter
      each consignment has a unique TransferCompleteDatetime to support date filters

    there are 28 file objects (1 to 28) associated with consignments
      file_1 associated to consignment_1
      file_2 and file_3 associated to consignment_2
      file_4 , file_5 and file_6 associated to consignment_3
      file_7 , file_8, file_9 and file_10 associated to consignment_4
      file_11 associated to consignment_5
      file_12 and file_3 associated to consignment_6
      file_14 , file_15 and file_16 associated to consignment_7
      file_17 , file_18 and file_19 associated to consignment_8
      file_20 and file_21 associated to consignment_9
      file_22 , file_23, file_24 and file_25 associated to consignment_10
      file_26 and file_27 associated to consignment_11
      file_28 associated to consignment_12
    """

    body_1 = BodyFactory(Name="first_body", Description="first_body")
    body_2 = BodyFactory(Name="second_body", Description="second_body")
    body_3 = BodyFactory(Name="third_body", Description="third_body")
    body_4 = BodyFactory(Name="fourth_body", Description="fourth_body")
    body_5 = BodyFactory(Name="fifth_body", Description="fifth_body")
    body_6 = BodyFactory(Name="sixth_body", Description="sixth_body")

    series_1 = SeriesFactory(
        Name="first_series", Description="first_series", body_series=body_1
    )
    series_2 = SeriesFactory(
        Name="second_series", Description="second_series", body_series=body_2
    )
    series_3 = SeriesFactory(
        Name="third_series", Description="third_series", body_series=body_3
    )
    series_4 = SeriesFactory(
        Name="fourth_series", Description="fourth_series", body_series=body_4
    )
    series_5 = SeriesFactory(
        Name="fifth_series", Description="fifth_series", body_series=body_5
    )

    series_6 = SeriesFactory(
        Name="sixth_series", Description="sixth_series", body_series=body_6
    )
    series_7 = SeriesFactory(
        Name="seventh_series", Description="seventh_series", body_series=body_6
    )

    consignment_1 = ConsignmentFactory(
        consignment_series=series_1,
        consignment_bodies=body_1,
        ConsignmentReference="TDR-2023-FI1",
        TransferCompleteDatetime="2023-01-13",
    )
    consignment_2 = ConsignmentFactory(
        consignment_series=series_1,
        consignment_bodies=body_1,
        ConsignmentReference="TDR-2023-SE2",
        TransferCompleteDatetime="2023-02-7",
    )

    consignment_3 = ConsignmentFactory(
        consignment_series=series_2,
        consignment_bodies=body_2,
        ConsignmentReference="TDR-2023-TH3",
        TransferCompleteDatetime="2023-03-15",
    )
    consignment_4 = ConsignmentFactory(
        consignment_series=series_2,
        consignment_bodies=body_2,
        ConsignmentReference="TDR-2023-FO4",
        TransferCompleteDatetime="2023-04-26",
    )

    consignment_5 = ConsignmentFactory(
        consignment_series=series_3,
        consignment_bodies=body_3,
        ConsignmentReference="TDR-2023-FI5",
        TransferCompleteDatetime="2023-05-10",
    )
    consignment_6 = ConsignmentFactory(
        consignment_series=series_3,
        consignment_bodies=body_3,
        ConsignmentReference="TDR-2023-SI6",
        TransferCompleteDatetime="2023-06-17",
    )

    consignment_7 = ConsignmentFactory(
        consignment_series=series_4,
        consignment_bodies=body_4,
        ConsignmentReference="TDR-2023-SE7",
        TransferCompleteDatetime="2023-07-21",
    )
    consignment_8 = ConsignmentFactory(
        consignment_series=series_4,
        consignment_bodies=body_4,
        ConsignmentReference="TDR-2023-EI8",
        TransferCompleteDatetime="2023-08-3",
    )

    consignment_9 = ConsignmentFactory(
        consignment_series=series_5,
        consignment_bodies=body_5,
        ConsignmentReference="TDR-2023-NI9",
        TransferCompleteDatetime="2023-09-21",
    )
    consignment_10 = ConsignmentFactory(
        consignment_series=series_5,
        consignment_bodies=body_5,
        ConsignmentReference="TDR-2023-TE10",
        TransferCompleteDatetime="2023-09-21",
    )

    consignment_11 = ConsignmentFactory(
        consignment_series=series_6,
        consignment_bodies=body_6,
        ConsignmentReference="TDR-2023-EL11",
        TransferCompleteDatetime="2023-10-14",
    )
    consignment_12 = ConsignmentFactory(
        consignment_series=series_7,
        consignment_bodies=body_6,
        ConsignmentReference="TDR-2023-TW12",
        TransferCompleteDatetime="2023-11-25",
    )

    file_1 = FileFactory(
        file_consignments=consignment_1,
        FileType="File",
        FileName="first_file.txt",
        FilePath="/data/first_file.txt",
    )

    file_2 = FileFactory(
        file_consignments=consignment_2,
        FileType="File",
        FileName="second_file.pdf",
        FilePath="/data/second_file.pdf",
    )

    file_3 = FileFactory(
        file_consignments=consignment_2,
        FileType="File",
        FileName="third_file.doc",
        FilePath="/data/third_file.doc",
    )

    file_4 = FileFactory(
        file_consignments=consignment_3,
        FileType="File",
        FileName="fourth_file.docx",
        FilePath="/data/fourth_file.docx",
    )

    file_5 = FileFactory(
        file_consignments=consignment_3,
        FileType="File",
        FileName="fifth_file.docx",
        FilePath="/data/fifth_file.docx",
    )

    file_6 = FileFactory(
        file_consignments=consignment_3,
        FileType="File",
        FileName="sixth_file.ppt",
        FilePath="/data/sixth_file.ppt",
    )

    file_7 = FileFactory(
        file_consignments=consignment_4,
        FileType="File",
        FileName="seventh_file.xls",
        FilePath="/data/seventh_file.xls",
    )

    file_8 = FileFactory(
        file_consignments=consignment_4,
        FileType="File",
        FileName="eighth_file.pdf",
        FilePath="/data/seventh_file.pdf",
    )

    file_9 = FileFactory(
        file_consignments=consignment_4,
        FileType="File",
        FileName="ninth_file.txt",
        FilePath="/data/ninth_file.txt",
    )

    file_10 = FileFactory(
        file_consignments=consignment_4,
        FileType="File",
        FileName="tenth_file.ppt",
        FilePath="/data/tenth_file.ppt",
    )

    file_11 = FileFactory(
        file_consignments=consignment_5,
        FileType="File",
        FileName="eleventh_file.zip",
        FilePath="/data/eleventh_file.zip",
    )

    file_12 = FileFactory(
        file_consignments=consignment_6,
        FileType="File",
        FileName="twelfth_file.ppt",
        FilePath="/data/twelfth_file.ppt",
    )

    file_13 = FileFactory(
        file_consignments=consignment_6,
        FileType="File",
        FileName="thirteenth_file.docx",
        FilePath="/data/thirteenth_file.docx",
    )

    file_14 = FileFactory(
        file_consignments=consignment_7,
        FileType="File",
        FileName="fourteenth_file.ppt",
        FilePath="/data/fourteenth_file.ppt",
    )

    file_15 = FileFactory(
        file_consignments=consignment_7,
        FileType="File",
        FileName="fifteenth_file.png",
        FilePath="/data/fifteenth_file.png",
    )

    file_16 = FileFactory(
        file_consignments=consignment_7,
        FileType="File",
        FileName="sixteenth_file.gif",
        FilePath="/data/sixteenth_file.gif",
    )

    file_17 = FileFactory(
        file_consignments=consignment_8,
        FileType="File",
        FileName="seventeenth_file.pdf",
        FilePath="/data/seventeenth_file.pdf",
    )

    file_18 = FileFactory(
        file_consignments=consignment_8,
        FileType="File",
        FileName="eighteenth_file.xls",
        FilePath="/data/eighteenth_file.xls",
    )

    file_19 = FileFactory(
        file_consignments=consignment_8,
        FileType="File",
        FileName="nineteenth_file.ppt",
        FilePath="/data/nineteenth_file.ppt",
    )

    file_20 = FileFactory(
        file_consignments=consignment_9,
        FileType="File",
        FileName="twentieth_file.tiff",
        FilePath="/data/twentieth_file.tiff",
    )

    file_21 = FileFactory(
        file_consignments=consignment_9,
        FileType="File",
        FileName="twenty-first.ppt",
        FilePath="/data/twenty-first.ppt",
    )

    file_22 = FileFactory(
        file_consignments=consignment_10,
        FileType="File",
        FileName="twenty-second.doc",
        FilePath="/data/twenty-second.doc",
    )

    file_23 = FileFactory(
        file_consignments=consignment_10,
        FileType="File",
        FileName="twenty-third.docx",
        FilePath="/data/twenty-third.docx",
    )

    file_24 = FileFactory(
        file_consignments=consignment_10,
        FileType="File",
        FileName="twenty-fourth.docx",
        FilePath="/data/twenty-fourth.docx",
    )

    file_25 = FileFactory(
        file_consignments=consignment_10,
        FileType="File",
        FileName="twenty-fifth.xls",
        FilePath="/data/twenty-fifth.xls",
    )

    file_26 = FileFactory(
        file_consignments=consignment_11,
        FileType="File",
        FileName="twenty-sixth.docx",
        FilePath="/data/twenty-sixth.docx",
    )

    file_27 = FileFactory(
        file_consignments=consignment_11,
        FileType="File",
        FileName="twenty-seventh.xls",
        FilePath="/data/twenty-seventh.xls",
    )

    file_28 = FileFactory(
        file_consignments=consignment_12,
        FileType="File",
        FileName="twenty-eighth.doc",
        FilePath="/data/twenty-eighth.doc",
    )

    return [
        file_1,
        file_2,
        file_3,
        file_4,
        file_5,
        file_6,
        file_7,
        file_8,
        file_9,
        file_10,
        file_11,
        file_12,
        file_13,
        file_14,
        file_15,
        file_16,
        file_17,
        file_18,
        file_19,
        file_20,
        file_21,
        file_22,
        file_23,
        file_24,
        file_25,
        file_26,
        file_27,
        file_28,
    ]
