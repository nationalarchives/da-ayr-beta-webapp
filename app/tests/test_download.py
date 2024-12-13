from unittest.mock import MagicMock, patch

import boto3
from flask.testing import FlaskClient
from moto import mock_aws

from app.tests.factories import FileFactory


def create_mock_s3_bucket_with_object(bucket_name, file):
    """
    Creates a dummy bucket to be used by tests
    """
    s3 = boto3.resource("s3", region_name="us-east-1")

    bucket = s3.create_bucket(Bucket=bucket_name)

    file_object = s3.Object(
        bucket_name, f"{file.consignment.ConsignmentReference}/{file.FileId}"
    )
    file_object.put(Body="record")
    return bucket


class TestDownload:
    @property
    def route_url(self):
        return "/download"

    def test_invalid_id_raises_404(self, client: FlaskClient):
        """
        Given a UUID, not corresponding to the id of a file in the database
        When a GET request is made to download route
        Then a 404 http response is returned
        """
        response = client.get(f"{self.route_url}/some-id")

        assert response.status_code == 404

    @mock_aws
    def test_download_record_standard_user_with_citable_reference_with_file_extension(
        self, app, client, mock_standard_user
    ):
        """
        Given a File in the database with corresponding file in the s3 bucket
        When a standard user with access to the file's transferring body makes a
            request to download record
        Then the response status code should be 200
        And the file should contain the expected content
        And the downloaded filename should be the File's CiteableReference with extension
        """
        bucket_name = "test_bucket"
        file = FileFactory(FileType="file", FileName="testfile.doc")

        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(
            client, file.consignment.series.body.Name, can_download=True
        )
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 200

        assert (
            response.headers["Content-Disposition"]
            == f"attachment; filename={file.CiteableReference}.doc"
        )
        assert response.data == b"record"

    @mock_aws
    def test_download_record_standard_user_with_citable_reference_without_file_extension(
        self, app, client, mock_standard_user
    ):
        """
        Given a File in the database with corresponding file in the s3 bucket
        When a standard user with access to the file's transferring body makes a
            request to download record
        Then the response status code should be 200
        And the file should contain the expected content
        And the downloaded filename should be the filename with extension
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file",
        )

        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(
            client, file.consignment.series.body.Name, can_download=True
        )
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 200

        assert (
            response.headers["Content-Disposition"]
            == f"attachment; filename={file.FileName}"
        )
        assert response.data == b"record"

    @mock_aws
    def test_download_record_standard_user_without_citable_reference(
        self, app, client, mock_standard_user
    ):
        """
        Given a File in the database with corresponding file in the s3 bucket
            without a CiteableReference
        When a standard user with access to the file's transferring body makes a
            request to download record
        Then the response status code should be 200
        And the file should contain the expected content
        And the downloaded filename should be fileName with extension
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file", FileName="testfile.doc", CiteableReference=None
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(
            client, file.consignment.series.body.Name, can_download=True
        )
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 200

        assert (
            response.headers["Content-Disposition"]
            == f"attachment; filename={file.FileName}"
        )
        assert response.data == b"record"

    @mock_aws
    def test_download_record_standard_user_get_file_errors(
        self, app, client, mock_standard_user
    ):
        """
        Given a file is requested from the database / S3 which doesn't exist
        When a standard user tries to access the file to download
        Then the response status code should be 404
        """

        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file", FileName="testimage.png", CiteableReference=None
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(
            client, file.consignment.series.body.Name, can_download=True
        )
        response = client.get(f"{self.route_url}/invalid_file")

        assert response.status_code == 404

    @mock_aws
    @patch("boto3.client")
    def test_download_record_standard_user_read_file_error(
        self, mock_boto3_client, app, client, mock_standard_user, caplog
    ):
        """
        Given a file in the database with corresponding file in the S3 bucket
            but reading the file content fails
        When a standard user with access to the file's transferring body makes a request to download the record
        Then the response status code should be 500
        """

        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file", FileName="testimage.png", CiteableReference=None
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        # Mock the S3 client and its get_object method
        mock_s3_client = MagicMock()
        mock_s3_client.get_object.return_value = {
            "Body": MagicMock(
                read=MagicMock(side_effect=Exception("Read error"))
            )
        }
        mock_boto3_client.return_value = mock_s3_client

        mock_standard_user(
            client, file.consignment.series.body.Name, can_download=True
        )

        response = client.get(f"{self.route_url}/{file.FileId}")

        msg = "Error reading S3 file content: Read error"

        assert response.status_code == 500
        assert caplog.records[1].levelname == "ERROR"
        assert caplog.records[1].message == msg

    @mock_aws
    def test_raises_404_for_standard_user_without_access_to_files_transferring_body(
        self, app, client, mock_standard_user
    ):
        """
        Given a File in the database
        When a standard user without access to the file's consignment body makes a
            request to download record
        Then the response status code should be 404
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file",
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(client, "different_body", can_download=True)
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 404

    @mock_aws
    def test_download_record_for_all_access_user_valid_response(
        self, app, client, mock_all_access_user
    ):
        """
        Given a File in the database
        And an all_access_user
        When the all_access_user makes a request to download record
        Then the response status code should be 200
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file",
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_all_access_user(client, can_download=True)
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 200

    @mock_aws
    def test_download_record_for_all_access_user_forbidden_response(
        self, app, client, mock_all_access_user
    ):
        """
        Given a File in the database
        And an all_access_user
        When the all_access_user with no download permissions makes a request to download record
        Then the response status code should be 401
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file",
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_all_access_user(client)
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 403

    @mock_aws
    def test_download_record_for_standard_user_forbidden_response(
        self, app, client, mock_standard_user
    ):
        """
        Given a File in the database
        And an all_access_user
        When the standard_user with no download permissions makes a request to download record
        Then the response status code should be 401
        """
        bucket_name = "test_bucket"
        file = FileFactory(
            FileType="file",
        )
        create_mock_s3_bucket_with_object(bucket_name, file)
        app.config["RECORD_BUCKET_NAME"] = bucket_name

        mock_standard_user(client, file.consignment.series.body.Name)
        response = client.get(f"{self.route_url}/{file.FileId}")

        assert response.status_code == 403
