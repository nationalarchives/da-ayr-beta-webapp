import uuid
from datetime import datetime
from unittest.mock import patch

import pytest
import werkzeug
from flask.testing import FlaskClient
from sqlalchemy import exc

from app.main.db.models import Body, db
from app.main.db.queries import (
    browse_data,
    fuzzy_search,
    get_file_metadata,
    get_user_accessible_transferring_bodies,
)
from app.tests.factories import (
    ConsignmentFactory,
    FileFactory,
    FileMetadataFactory,
)
from app.tests.mock_database import create_multiple_test_records

per_page = 5


class TestFuzzySearch:
    def test_fuzzy_search_blank_query_parameter(self, client: FlaskClient):
        """
        Given a query string not provided
        When fuzzy_search is called with it
        Then None is returned
        """

        query = ""
        result = fuzzy_search(query, page=1, per_page=per_page)
        assert result is None

    def test_fuzzy_search_no_results(self, client: FlaskClient):
        """
        Given a query string that does not match any field in any file object
            in the database
        When fuzzy_search is called with it
        Then an empty list is returned
        """

        query = "junk"
        result = fuzzy_search(query, page=1, per_page=per_page)
        assert result.items == []

    def test_fuzzy_search_with_single_record_result(self, client: FlaskClient):
        """
        Given multiple File objects in the database
            and a query string that matches some fields in only 1 of them
        When fuzzy_search is called with the query
        Then a list containing 1 dictionary with information for the corresponding
            file is returned
        """
        files = create_multiple_test_records()

        query = "test body2"
        result = fuzzy_search(query, page=1, per_page=per_page)
        assert result.items == [
            (
                "test body2",
                "test series2",
                "test consignment2",
                "test_file2.txt",
                files[1].file_consignments.consignment_bodies.BodyId,
                files[1].file_consignments.consignment_series.SeriesId,
            )
        ]

    def test_fuzzy_search_with_single_page_result(self, client: FlaskClient):
        """
        Given multiple File objects in the database
            and a query string that matches some fields in only 1 of them
        When fuzzy_search is called with the query
        Then a list containing 2 (max - per_page) dictionary with information for the corresponding
            file is returned
        and more than 1 page returned false
        and has_next return false
        """
        files = create_multiple_test_records()

        query = "test body1"
        result = fuzzy_search(query, page=1, per_page=per_page)
        assert result.items == [
            (
                "test body1",
                "test series1",
                "test consignment1",
                "test_file1.pdf",
                files[0].file_consignments.consignment_bodies.BodyId,
                files[0].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body11",
                "test series11",
                "test consignment11",
                "test_file11.txt",
                files[10].file_consignments.consignment_bodies.BodyId,
                files[10].file_consignments.consignment_series.SeriesId,
            ),
        ]
        assert result.pages == 1
        assert result.has_next is False

    def test_fuzzy_search_with_multiple_page_results(self, client: FlaskClient):
        """
        Given multiple File objects in the database
            and a query string that matches some fields in only 1 of them
        When fuzzy_search is called with the query
        Then a list containing 5 (per_page) dictionary with information for the corresponding
            file is returned
        and more than 1 page returned true
        and has_next return true
        """
        files = create_multiple_test_records()

        query = "testing body"
        result = fuzzy_search(query, page=1, per_page=per_page)
        assert result.items == [
            (
                "testing body10",
                "test series10",
                "test consignment10",
                "test_file10.txt",
                files[9].file_consignments.consignment_bodies.BodyId,
                files[9].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body11",
                "test series11",
                "test consignment11",
                "test_file11.txt",
                files[10].file_consignments.consignment_bodies.BodyId,
                files[10].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body3",
                "test series3",
                "test consignment3",
                "test_file3.pdf",
                files[2].file_consignments.consignment_bodies.BodyId,
                files[2].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body4",
                "test series4",
                "test consignment4",
                "test_file4.txt",
                files[3].file_consignments.consignment_bodies.BodyId,
                files[3].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body5",
                "test series5",
                "test consignment5",
                "test_file5.txt",
                files[4].file_consignments.consignment_bodies.BodyId,
                files[4].file_consignments.consignment_series.SeriesId,
            ),
        ]
        assert result.pages > 0
        assert result.has_next is True

    def test_fuzzy_search_get_specific_page_results(self, client: FlaskClient):
        """
        Given multiple File objects in the database
            and a query string that matches some fields in only 1 of them
        When fuzzy_search is called with the query
        Then a list containing 5 (per_page) dictionary with information for the corresponding
            file is returned for page 2
        """
        files = create_multiple_test_records()

        query = "testing body"
        result = fuzzy_search(query, page=2, per_page=per_page)
        assert result.items == [
            (
                "testing body6",
                "test series6",
                "test consignment6",
                "test_file6.txt",
                files[5].file_consignments.consignment_bodies.BodyId,
                files[5].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body7",
                "test series7",
                "test consignment7",
                "test_file7.txt",
                files[6].file_consignments.consignment_bodies.BodyId,
                files[6].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body8",
                "test series8",
                "test consignment8",
                "test_file8.txt",
                files[7].file_consignments.consignment_bodies.BodyId,
                files[7].file_consignments.consignment_series.SeriesId,
            ),
            (
                "testing body9",
                "test series9",
                "test consignment9",
                "test_file9.txt",
                files[8].file_consignments.consignment_bodies.BodyId,
                files[8].file_consignments.consignment_series.SeriesId,
            ),
        ]
        assert result.pages > 0
        assert result.has_next is False
        assert result.has_prev is True


class TestBrowseData:
    def test_browse_data_without_filters(self, client: FlaskClient):
        """
        Given multiple File objects in the database
        When browse_data is called with page=2, per_page=5
        Then it returns a Paginate object returning the first 5 items
            ordered by Body name then Series name
        """
        files = create_multiple_test_records()
        result = browse_data(page=1, per_page=5)

        assert result.items == [
            (
                files[0].file_consignments.consignment_bodies.BodyId,
                "test body1",
                files[0].file_consignments.consignment_series.SeriesId,
                "test series1",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[1].file_consignments.consignment_bodies.BodyId,
                "test body2",
                files[1].file_consignments.consignment_series.SeriesId,
                "test series2",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[9].file_consignments.consignment_bodies.BodyId,
                "testing body10",
                files[9].file_consignments.consignment_series.SeriesId,
                "test series10",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[10].file_consignments.consignment_bodies.BodyId,
                "testing body11",
                files[10].file_consignments.consignment_series.SeriesId,
                "test series11",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[2].file_consignments.consignment_bodies.BodyId,
                "testing body3",
                files[2].file_consignments.consignment_series.SeriesId,
                "test series3",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
        ]

    def test_browse_data_get_specific_page_results(self, client: FlaskClient):
        """
        Given multiple File objects in the database
        When browse_data is called with page=2, per_page=5
        Then it returns a Paginate object returning the second 5 items
            ordered by Body name then Series name
        """
        files = create_multiple_test_records()

        result = browse_data(page=2, per_page=per_page)
        assert result.items == [
            (
                files[3].file_consignments.consignment_bodies.BodyId,
                "testing body4",
                files[3].file_consignments.consignment_series.SeriesId,
                "test series4",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[4].file_consignments.consignment_bodies.BodyId,
                "testing body5",
                files[4].file_consignments.consignment_series.SeriesId,
                "test series5",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[5].file_consignments.consignment_bodies.BodyId,
                "testing body6",
                files[5].file_consignments.consignment_series.SeriesId,
                "test series6",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[6].file_consignments.consignment_bodies.BodyId,
                "testing body7",
                files[6].file_consignments.consignment_series.SeriesId,
                "test series7",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
            (
                files[7].file_consignments.consignment_bodies.BodyId,
                "testing body8",
                files[7].file_consignments.consignment_series.SeriesId,
                "test series8",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            ),
        ]
        assert result.pages > 0
        assert result.has_next is True
        assert result.has_prev is True

    def test_browse_data_with_transferring_body_filter(
        self, client: FlaskClient
    ):
        """
        Given multiple File objects in the database and a transferring_body_id
            that matches only one of them
        When browse_data is called with transferring_body_id
        Then it returns a list containing 1 dictionary for the matching record with
            expected fields
        """
        files = create_multiple_test_records()

        file = files[0]

        transferring_body_id = file.file_consignments.consignment_bodies.BodyId
        series_id = file.file_consignments.consignment_series.SeriesId
        result = browse_data(
            page=1, per_page=per_page, transferring_body_id=transferring_body_id
        )

        assert result.items == [
            (
                transferring_body_id,
                "test body1",
                series_id,
                "test series1",
                datetime(2023, 1, 1, 0, 0),
                1,
                1,
            )
        ]

    def test_browse_data_with_series_filter(self, client: FlaskClient):
        """
        Given multiple File objects in the database and a series_id
            that matches only one of them
        When browse_data is called with series_id
        Then it returns a list containing 1 dictionary for the matching record with
            expected fields
        """
        files = create_multiple_test_records()

        file = files[0]

        transferring_body_id = file.file_consignments.consignment_bodies.BodyId
        series_id = file.file_consignments.consignment_series.SeriesId
        consignment_id = file.file_consignments.ConsignmentId

        result = browse_data(page=1, per_page=per_page, series_id=series_id)

        assert result.items == [
            (
                transferring_body_id,
                "test body1",
                series_id,
                "test series1",
                datetime(2023, 1, 1, 0, 0),
                1,
                consignment_id,
                "test consignment1",
            )
        ]

    def test_browse_data_with_consignment_filter(self, app):
        """
        Given three file objects with associated metadata part of 1 consignment,
            where 2 file types is 'file', another file 'folder', and another file of
            type 'file' and metadata associated with a different consignment
        When I call the 'browse_data' function with the consignment id
            of the first 3 file objects
        Then it returns a Pagination object with 2 total results corresponding to the
            first 2 files, ordered by their names and with the expected metadata values
        """
        consignment = ConsignmentFactory()

        file_1 = FileFactory(
            file_consignments=consignment, FileName="file_1", FileType="file"
        )

        file_1_metadata = {
            "date_last_modified": "2023-02-25T10:12:47",
            "closure_type": "Closed",
            "closure_start_date": "2023-02-25T11:14:34",
            "closure_period": "50",
        }

        [
            FileMetadataFactory(
                file_metadata=file_1,
                PropertyName=property_name,
                Value=value,
            )
            for property_name, value in file_1_metadata.items()
        ]

        file_2 = FileFactory(
            file_consignments=consignment, FileName="file_2", FileType="file"
        )

        file_2_metadata = {
            "date_last_modified": "2023-02-27T12:28:08",
            "closure_type": "Open",
            "closure_start_date": None,
            "closure_period": None,
        }

        [
            FileMetadataFactory(
                file_metadata=file_2,
                PropertyName=property_name,
                Value=value,
            )
            for property_name, value in file_2_metadata.items()
        ]

        FileFactory(file_consignments=consignment, FileType="folder")

        FileFactory(FileType="file")

        pagination_object = browse_data(
            page=1, per_page=per_page, consignment_id=consignment.ConsignmentId
        )

        assert pagination_object.total == 2

        expected_results = [
            (
                file_1.FileId,
                "file_1",
                "2023-02-25T10:12:47",
                "Closed",
                "2023-02-25T11:14:34",
                "50",
            ),
            (
                file_2.FileId,
                "file_2",
                "2023-02-27T12:28:08",
                "Open",
                None,
                None,
            ),
        ]

        results = pagination_object.items

        assert results == expected_results


class TestGetFileMetadata:
    def test_invalid_uuid_raises_not_found_error(self, client: FlaskClient):
        """
        Given a UUID not corresponding to the id of a file in the database
        When get_file_metadata is called with it
        Then werkzeug.exceptions.NotFound is raised
        """
        non_existent_file_id = uuid.uuid4()
        with pytest.raises(werkzeug.exceptions.NotFound):
            get_file_metadata(non_existent_file_id)

    def test_valid_uuid_returns_metadata(self, client: FlaskClient):
        """
        Given a file with associated metadata,
        When get_file_metadata is called with its UUID,
        Then a tuple of specific metadata for the file is returned
        """
        file = FileFactory(FileName="test_file.txt", FileType="file")

        metadata = {
            "date_last_modified": "2023-02-25T10:12:47",
            "closure_type": "Closed",
            "description": "Test description",
            "held_by": "Test holder",
            "legal_status": "Test legal status",
            "rights_copyright": "Test copyright",
            "language": "English",
        }

        [
            FileMetadataFactory(
                file_metadata=file,
                PropertyName=property_name,
                Value=value,
            )
            for property_name, value in metadata.items()
        ]

        assert get_file_metadata(file_id=file.FileId) == {
            "file_id": file.FileId,
            "file_name": "test_file.txt",
            "status": "Closed",
            "description": "Test description",
            "date_last_modified": "2023-02-25T10:12:47",
            "held_by": "Test holder",
            "legal_status": "Test legal status",
            "rights_copyright": "Test copyright",
            "language": "English",
            "consignment_id": file.ConsignmentId,
            "transferring_body": file.file_consignments.consignment_bodies.Name,
        }


class TestGetUserAccessibleTransferringBodies:
    def test_no_token_returns_empty_list(
        self,
    ):
        """
        Given no access token,
        When calling the get_user_transferring_body_keycloak_groups
        Then it should return an empty list
        """
        results = get_user_accessible_transferring_bodies(None)
        assert results == []

    @patch("app.main.db.queries.decode_token")
    def test_inactive_token_returns_empty_list(self, mock_decode_token):
        """
        Given an inactive access token
        When calling get_user_transferring_body_keycloak_groups with it
        Then it should return an empty list
        """
        mock_decode_token.return_value = {
            "active": False,
        }
        assert get_user_accessible_transferring_bodies("access_token") == []

    @patch("app.main.db.queries.decode_token")
    def test_no_transferring_bodies_returns_empty_list(
        self,
        mock_decode_token,
    ):
        """
        Given an access token which once decoded contains 2 transferring body groups
        When I call get_user_accessible_transferring_bodies with it
        Then it should return a list with the 2 corresponding body names
        """
        mock_decode_token.return_value = {
            "active": True,
            "groups": [
                "/something_else/test body1",
                "/something_else/test body2",
                "/ayr_user/bar",
            ],
        }
        results = get_user_accessible_transferring_bodies("access_token")
        assert results == []

    @patch("app.main.db.queries.decode_token")
    def test_transferring_bodies_in_groups_returns_corresponding_body_names(
        self, mock_decode_token, client: FlaskClient
    ):
        """
        Given an access token which once decoded contains 2 groups prefixed with
            /transferring_body_user/
            and another group
            and 2 corresponding bodies in the database
            and an extra body in the database
        When get_user_accessible_transferring_bodies is called with it
        Then it should return a list with the 2 corresponding body names
        """
        body_1 = Body(
            BodyId=uuid.uuid4(), Name="test body1", Description="test body1"
        )
        db.session.add(body_1)
        db.session.commit()

        body_2 = Body(
            BodyId=uuid.uuid4(), Name="test body2", Description="test body2"
        )
        db.session.add(body_2)
        db.session.commit()

        body_3 = Body(
            BodyId=uuid.uuid4(), Name="test body3", Description="test body3"
        )
        db.session.add(body_3)
        db.session.commit()

        mock_decode_token.return_value = {
            "active": True,
            "groups": [
                "/transferring_body_user/test body1",
                "/transferring_body_user/test body2",
                "/foo/bar",
            ],
        }
        results = get_user_accessible_transferring_bodies("access_token")
        assert results == ["test body1", "test body2"]

    @patch("app.main.db.queries.db")
    @patch("app.main.db.queries.decode_token")
    def test_db_raised_exception_returns_empty_list_and_log_message(
        self, mock_decode_token, database, capsys, client
    ):
        """
        Given a db execution error
        When get_user_accessible_transferring_bodies is called
        Then the list should be empty and an error message is logged
        """
        mock_decode_token.return_value = {
            "active": True,
            "groups": [
                "/transferring_body_user/test body1",
                "/transferring_body_user/test body2",
                "/ayr_user/bar",
            ],
        }

        def mock_execute(_):
            raise exc.SQLAlchemyError("foo bar")

        database.session.execute.side_effect = mock_execute

        results = get_user_accessible_transferring_bodies("access_token")
        assert results == []
        assert (
            "Failed to return results from database with error : foo bar"
            in capsys.readouterr().out
        )
