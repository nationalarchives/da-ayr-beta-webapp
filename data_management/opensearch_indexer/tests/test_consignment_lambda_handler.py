import json
from unittest.mock import patch
from uuid import uuid4

import boto3
import botocore
from moto import mock_aws
from opensearch_indexer.index_consignment.lambda_function import lambda_handler
from requests_aws4auth import AWS4Auth
from sqlalchemy.orm import sessionmaker

from data_management.opensearch_indexer.opensearch_indexer.text_extraction import (
    TextExtractionStatus,
)
from data_management.opensearch_indexer.tests.conftest import (
    Body,
    Consignment,
    File,
    FileMetadata,
    Series,
)

# Original botocore _make_api_call function
orig = botocore.client.BaseClient._make_api_call


# Mocked botocore _make_api_call function
def mock_make_api_call(self, operation_name, kwarg):
    if operation_name == "AssumeRole":
        return {
            "Credentials": {
                "AccessKeyId": "test_access_key",
                "SecretAccessKey": "test_secret_key",  # pragma: allowlist secret
                "SessionToken": "test_token",
                "Expiration": "2024-09-18T12:00:00Z",
            }
        }
    return orig(self, operation_name, kwarg)


# @patch(
#     "opensearch_indexer.index_consignment.bulk_index_consignment._build_db_url"
# )
@mock_aws
def test_lambda_handler_calls_index_file_content_and_metadata_in_opensearch(
    monkeypatch, temp_db
):
    """
    Given:
    - An S3 bucket containing a file.
    - A secret in AWS Secrets Manager with secret name specified in environment variable `SECRET_ID`
        including database and OpenSearch connection details including an IAM role.

    When:
    - The lambda_handler function is triggered by an S3 event.

    Then:
    - The index_file_content_and_metadata_in_opensearch function is called with the correct parameters:
      - The file name "test-file.txt".
      - The file content b"Test file content".
      - The database connection string.
      - The OpenSearch host URL.
      - An AWS4Auth object with the correct credentials determined by assuming the IAM role.
    """
    secret_name = "test_vars"  # pragma: allowlist secret

    monkeypatch.setenv("SECRET_ID", secret_name)

    bucket_name = "test_bucket"

    opensearch_master_role_arn = (
        "arn:aws:iam::123456789012:role/test-opensearch-role"
    )
    breakpoint()
    secret_string = json.dumps(
        {
            "DB_USER": temp_db.url.username if temp_db.url.username else "",
            "DB_PASSWORD": (
                temp_db.url.password if temp_db.url.password else ""
            ),  # pragma: allowlist secret
            "DB_HOST": temp_db.url.host,
            "DB_PORT": temp_db.url.port if temp_db.url.port else "",
            "DB_NAME": temp_db.url.database if temp_db.url.database else "",
            "AWS_REGION": "eu-west-2",
            "RECORD_BUCKET_NAME": bucket_name,
            "OPEN_SEARCH_HOST": "https://test-opensearch.com",
            "OPEN_SEARCH_MASTER_ROLE_ARN": opensearch_master_role_arn,
            "OPEN_SEARCH_BULK_INDEX_TIMEOUT": 600,
        }
    )

    # mock_build_db_url.return_value = str(temp_db.url)

    secretsmanager_client = boto3.client(
        "secretsmanager", region_name="eu-west-2"
    )

    secretsmanager_client.create_secret(
        Name=secret_name, SecretString=secret_string
    )

    s3_client = boto3.client("s3", region_name="us-east-1")

    body_id = uuid4()
    series_id = uuid4()
    consignment_id = uuid4()

    body_id_hex = body_id.hex
    series_id_hex = series_id.hex
    consignment_id_hex = consignment_id.hex

    consignment_reference = "TDR-2024-ABCD"

    file_1_id = uuid4()
    file_2_id = uuid4()
    file_3_id = uuid4()

    file_1_id_hex = file_1_id.hex
    file_2_id_hex = file_2_id.hex
    file_3_id_hex = file_3_id.hex

    Session = sessionmaker(bind=temp_db)
    with Session() as session:

        session.add_all(
            [
                File(
                    FileId=file_1_id,
                    FileType="File",
                    FileName="test-document.txt",
                    FileReference="file-123",
                    FilePath="/path/to/file",
                    CiteableReference="cite-ref-123",
                    ConsignmentId=consignment_id,
                ),
                File(
                    FileId=file_2_id,
                    FileType="File",
                    FileName="test-document.txt",
                    FileReference="file-123",
                    FilePath="/path/to/file",
                    CiteableReference="cite-ref-123",
                    ConsignmentId=consignment_id,
                ),
                File(
                    FileId=file_3_id,
                    FileType="File",
                    FileName="test-document.txt",
                    FileReference="file-123",
                    FilePath="/path/to/file",
                    CiteableReference="cite-ref-123",
                    ConsignmentId=consignment_id,
                ),
                Consignment(
                    ConsignmentId=consignment_id,
                    ConsignmentType="foo",
                    ConsignmentReference=consignment_reference,
                    SeriesId=series_id,
                ),
                Series(SeriesId=series_id, Name="series-name", BodyId=body_id),
                Body(
                    BodyId=body_id,
                    Name="body-name",
                    Description="transferring body description",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_1_id,
                    PropertyName="Key1",
                    Value="Value1",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_1_id,
                    PropertyName="Key2",
                    Value="Value2",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_2_id,
                    PropertyName="Key3",
                    Value="Value3",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_2_id,
                    PropertyName="Key4",
                    Value="Value4",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_3_id,
                    PropertyName="Key5",
                    Value="Value5",
                ),
                FileMetadata(
                    MetadataId=uuid4(),
                    FileId=file_3_id,
                    PropertyName="Key6",
                    Value="Value6",
                ),
            ]
        )
        session.commit()

        object_key_1 = f"{consignment_reference}/{file_1_id.hex}"
        object_key_2 = f"{consignment_reference}/{file_2_id.hex}"
        object_key_3 = f"{consignment_reference}/{file_3_id.hex}"

        s3_client.create_bucket(Bucket=bucket_name)

        s3_client.put_object(
            Bucket=bucket_name, Key=object_key_1, Body=b"Test file content"
        )
        s3_client.put_object(Bucket=bucket_name, Key=object_key_2, Body=b"")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key_3,
            Body=b"File content but in file we do not support text extraction for",
        )

        sns_message = {
            "properties": {
                "messageType": "uk.gov.nationalarchives.da.messages.ayrmetadata.loaded",
                "function": "ddt-ayrmetadataload-process",
            },
            "parameters": {
                "reference": consignment_reference,
                "originator": "DDT",
            },
        }

        event = {
            "Records": [
                {
                    "Sns": {
                        "Message": json.dumps(sns_message),
                    },
                }
            ]
        }

        with patch(
            "botocore.client.BaseClient._make_api_call", new=mock_make_api_call
        ):
            with patch(
                "opensearch_indexer.index_consignment.bulk_index_consignment.bulk_index_files_in_opensearch"
            ) as mock_bulk_index_files_in_opensearch:
                lambda_handler(event, None)

                args, _ = mock_bulk_index_files_in_opensearch.call_args

                assert args[0] == [
                    {
                        "file_id": file_1_id_hex,
                        "document": {
                            "file_id": file_1_id_hex,
                            "file_name": "test-document.txt",
                            "file_reference": "file-123",
                            "file_path": "/path/to/file",
                            "citeable_reference": "cite-ref-123",
                            "series_id": series_id_hex,
                            "series_name": "series-name",
                            "transferring_body": "body-name",
                            "transferring_body_id": body_id_hex,
                            "transferring_body_description": "transferring body description",
                            "consignment_id": consignment_id_hex,
                            "consignment_reference": "TDR-2024-ABCD",
                            "Key1": "Value1",
                            "Key2": "Value2",
                            "content": "Test file content",
                            "text_extraction_status": TextExtractionStatus.SUCCEEDED.value,
                        },
                    },
                    {
                        "document": {
                            "file_id": file_2_id_hex,
                            "file_name": "test-document.txt",
                            "file_reference": "file-123",
                            "file_path": "/path/to/file",
                            "citeable_reference": "cite-ref-123",
                            "series_id": series_id_hex,
                            "series_name": "series-name",
                            "transferring_body": "body-name",
                            "transferring_body_id": body_id_hex,
                            "transferring_body_description": "transferring body description",
                            "consignment_id": consignment_id_hex,
                            "consignment_reference": "TDR-2024-ABCD",
                            "Key3": "Value3",
                            "Key4": "Value4",
                            "content": "",
                            "text_extraction_status": TextExtractionStatus.SUCCEEDED.value,
                        },
                        "file_id": file_2_id_hex,
                    },
                    {
                        "document": {
                            "file_id": file_3_id_hex,
                            "file_name": "test-document.txt",
                            "file_reference": "file-123",
                            "file_path": "/path/to/file",
                            "citeable_reference": "cite-ref-123",
                            "series_id": series_id_hex,
                            "series_name": "series-name",
                            "consignment_id": consignment_id_hex,
                            "consignment_reference": "TDR-2024-ABCD",
                            "transferring_body": "body-name",
                            "transferring_body_id": body_id_hex,
                            "transferring_body_description": "transferring body description",
                            "Key5": "Value5",
                            "Key6": "Value6",
                            "content": "File content but in file we do not support text extraction for",
                            "text_extraction_status": TextExtractionStatus.SUCCEEDED.value,
                        },
                        "file_id": file_3_id_hex,
                    },
                ]
                assert args[1] == "https://test-opensearch.com"

                aws_auth = args[2]
                assert isinstance(aws_auth, AWS4Auth)
                assert aws_auth.access_id == "test_access_key"
                assert (
                    aws_auth.signing_key.secret_key
                    == "test_secret_key"  # pragma: allowlist secret
                )
                assert aws_auth.region == "eu-west-2"
                assert aws_auth.service == "es"
                assert aws_auth.session_token == "test_token"

                assert args[3] == 600
                assert args[4] is None
