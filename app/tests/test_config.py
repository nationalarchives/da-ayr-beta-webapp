import inspect
import json
from unittest.mock import patch

import boto3
import botocore
import pytest
from moto import mock_aws
from requests_aws4auth import AWS4Auth

from configs.aws_secrets_manager_config import AWSSecretsManagerConfig
from configs.env_config import EnvConfig

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


def test_local_env_vars_config_initialized(monkeypatch):
    """
    GIVEN environment variables are set without DEFAULT_AWS_PROFILE
    WHEN Config is initialized
    THEN it should have attributes with the expected environment variables
    """
    monkeypatch.setenv(
        "SQLALCHEMY_DATABASE_URI", "test_sqlalchemy_database_uri"
    )
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_HOST", "test_db_host")
    monkeypatch.setenv("DB_USER", "test_db_user")
    monkeypatch.setenv("DB_PASSWORD", "test_db_password")
    monkeypatch.setenv("DB_NAME", "test_db_name")
    monkeypatch.setenv(
        "DB_SSL_ROOT_CERTIFICATE", "test_db_ssl_root_certificate"
    )
    monkeypatch.setenv("AWS_SM_KEYCLOAK_CLIENT_SECRET_ID", "")
    monkeypatch.setenv("KEYCLOAK_BASE_URI", "test_keycloak_base_uri")
    monkeypatch.setenv("KEYCLOAK_CLIENT_ID", "test_keycloak_client_id")
    monkeypatch.setenv("KEYCLOAK_REALM_NAME", "test_keycloak_realm_name")
    monkeypatch.setenv(
        "KEYCLOAK_CLIENT_SECRET", "test_keycloak_client_secret"
    )  # pragma: allowlist secret
    monkeypatch.setenv(
        "SECRET_KEY", "test_secret_key"  # pragma: allowlist secret
    )
    monkeypatch.setenv("DEFAULT_PAGE_SIZE", 10)
    monkeypatch.setenv("DEFAULT_DATE_FORMAT", "test_default_date_format")
    monkeypatch.setenv("RECORD_BUCKET_NAME", "test_record_bucket_name")
    monkeypatch.setenv("FLASKS3_ACTIVE", "False")
    monkeypatch.setenv("FLASKS3_CDN_DOMAIN", "test_flasks3_cdn_domain")
    monkeypatch.setenv("FLASKS3_BUCKET_NAME", "test_flasks3_bucket_name")
    monkeypatch.setenv("PERF_TEST", "False")
    monkeypatch.setenv("OPEN_SEARCH_HOST", "test_os_host")
    monkeypatch.setenv("OPEN_SEARCH_USERNAME", "test_os_username")
    monkeypatch.setenv("OPEN_SEARCH_PASSWORD", "test_os_password")
    monkeypatch.setenv("OPEN_SEARCH_TIMEOUT", 10)

    config = EnvConfig()

    assert (
        config.SQLALCHEMY_DATABASE_URI == "postgresql+psycopg2://test_db_user:"
        "test_db_password@test_db_host:5432/test_db_name?sslmode=verify-full&sslrootcert=test_db_ssl_root_certificate"
    )
    assert config.KEYCLOAK_BASE_URI == "test_keycloak_base_uri"
    assert config.KEYCLOAK_CLIENT_ID == "test_keycloak_client_id"
    assert config.KEYCLOAK_REALM_NAME == "test_keycloak_realm_name"
    assert (
        config.KEYCLOAK_CLIENT_SECRET
        == "test_keycloak_client_secret"  # pragma: allowlist secret
    )
    assert config.SECRET_KEY == "test_secret_key"  # pragma: allowlist secret
    assert config.DEFAULT_PAGE_SIZE == 10
    assert config.DEFAULT_DATE_FORMAT == "test_default_date_format"
    assert config.RECORD_BUCKET_NAME == "test_record_bucket_name"
    assert config.FLASKS3_ACTIVE is False
    assert config.FLASKS3_CDN_DOMAIN == "test_flasks3_cdn_domain"
    assert config.FLASKS3_BUCKET_NAME == "test_flasks3_bucket_name"
    assert config.PERF_TEST is False
    assert config.OPEN_SEARCH_HOST == "test_os_host"
    assert config.OPEN_SEARCH_HTTP_AUTH == (
        "test_os_username",
        "test_os_password",
    )
    assert config.OPEN_SEARCH_TIMEOUT == 10


def test_local_env_config_variable_not_set_error(monkeypatch):
    """
    GIVEN an environment variable 'DEFAULT_DATE_FORMAT' is not set in local .env file
    WHEN Config is initialized
    THEN it should raise an exception with error
    """
    monkeypatch.setenv(
        "SQLALCHEMY_DATABASE_URI", "test_sqlalchemy_database_uri"
    )
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_HOST", "test_db_host")
    monkeypatch.setenv("DB_USER", "test_db_user")
    monkeypatch.setenv("DB_PASSWORD", "test_db_password")
    monkeypatch.setenv("DB_NAME", "test_db_name")
    monkeypatch.setenv(
        "DB_SSL_ROOT_CERTIFICATE", "test_db_ssl_root_certificate"
    )
    monkeypatch.setenv("KEYCLOAK_BASE_URI", "test_keycloak_base_uri")
    monkeypatch.setenv("KEYCLOAK_CLIENT_ID", "test_keycloak_client_id")
    monkeypatch.setenv("KEYCLOAK_REALM_NAME", "test_keycloak_realm_name")
    monkeypatch.setenv(
        "KEYCLOAK_CLIENT_SECRET", "test_keycloak_client_secret"
    )  # pragma: allowlist secret
    monkeypatch.setenv(
        "SECRET_KEY", "test_secret_key"  # pragma: allowlist secret
    )
    monkeypatch.setenv("DEFAULT_PAGE_SIZE", 10)
    monkeypatch.setenv("RECORD_BUCKET_NAME", "test_record_bucket_name")
    monkeypatch.setenv("AWS_REGION", "test_region")
    monkeypatch.setenv("FLASKS3_ACTIVE", "False")
    monkeypatch.setenv("FLASKS3_CDN_DOMAIN", "test_flasks3_cdn_domain")
    monkeypatch.setenv("FLASKS3_BUCKET_NAME", "test_flasks3_bucket_name")
    monkeypatch.setenv("PERF_TEST", "False")
    monkeypatch.setenv("OPEN_SEARCH_HOST", "test_os_host")
    monkeypatch.setenv("OPEN_SEARCH_USERNAME", "test_os_username")
    monkeypatch.setenv("OPEN_SEARCH_PASSWORD", "test_os_password")
    monkeypatch.setenv("OPEN_SEARCH_TIMEOUT", 10)
    monkeypatch.setenv("CSP_CONNECT_SRC", "")
    monkeypatch.setenv("CSP_DEFAULT_SRC", "")
    monkeypatch.setenv("CSP_FRAME_SRC", "")
    monkeypatch.setenv("CSP_IMG_SRC", "")
    monkeypatch.setenv("CSP_OBJECT_SRC", "")
    monkeypatch.setenv("CSP_SCRIPT_SRC", "")
    monkeypatch.setenv("CSP_SCRIPT_SRC_ELEM", "")
    monkeypatch.setenv("CSP_STYLE_SRC", "")
    monkeypatch.setenv("CSP_STYLE_SRC_ELEM", "")
    monkeypatch.setenv("CSP_WORKER_SRC", "")

    config = EnvConfig()

    with pytest.raises(KeyError) as error:
        inspect.getmembers(config)

    assert str(error.value) == "'DEFAULT_DATE_FORMAT'"


@mock_aws
def test_aws_secrets_manager_config_initialized(monkeypatch):
    """
    GIVEN AWS secret with secret_ids`AWS_SM_CONFIG_SECRET_ID`,
        `AWS_SM_KEYCLOAK_CLIENT_SECRET_ID` and `AWS_SM_DB_CONFIG_SECRET_ID`
        set with all config key value pairs
    WHEN Config is initialized
    THEN it should have attributes with the expected values from the AWS Secrets Manager secret
    """
    secret_value = json.dumps(
        {
            "AWS_REGION": "test_aws_region",
            "KEYCLOAK_BASE_URI": "test_keycloak_base_uri",
            "KEYCLOAK_CLIENT_ID": "test_keycloak_client_id",
            "KEYCLOAK_REALM_NAME": "test_keycloack_realm_name",
            "RECORD_BUCKET_NAME": "test_record_bucket_name",
            "FLASKS3_ACTIVE": "False",
            "FLASKS3_CDN_DOMAIN": "test_flasks3_cdn_domain",
            "PERF_TEST": "False",
            "FLASKS3_BUCKET_NAME": "test_flasks3_bucket_name",
            "DEFAULT_DATE_FORMAT": "test_default_date_format",
            "SECRET_KEY": "test_secret_key",  # pragma: allowlist secret,
            "DB_SSL_ROOT_CERTIFICATE": "test_db_ssl_root_certificate",
            "DEFAULT_PAGE_SIZE": 10,
            "OPEN_SEARCH_MASTER_ROLE_ARN": "test_master_role_arn",
            "OPEN_SEARCH_HOST": "test_os_host",  # pragma: allowlist secret
            "OPEN_SEARCH_TIMEOUT": 10,  # pragma: allowlist secret
        }
    )

    secret_kc_value = json.dumps({"SECRET": "test_keycloak_client_secret"})

    secret_db_value = json.dumps(
        {
            "username": "test_db_user",
            "password": "test_db_password",  # pragma: allowlist secret
            "port": "5432",
            "proxy": "test_db_host",
            "dbname": "test_db_name",
        }
    )

    ssm_client = boto3.client("secretsmanager")

    ssm_client.create_secret(
        Name="test_secret_id",
        SecretString=secret_value,
    )

    ssm_client.create_secret(
        Name="test_kc_secret_id",
        SecretString=secret_kc_value,
    )

    ssm_client.create_secret(
        Name="test_db_config_secret_id",
        SecretString=secret_db_value,
    )

    monkeypatch.setenv(
        "AWS_SM_CONFIG_SECRET_ID", "test_secret_id"
    )  # pragma: allowlist secret

    monkeypatch.setenv(
        "AWS_SM_KEYCLOAK_CLIENT_SECRET_ID", "test_kc_secret_id"
    )  # pragma: allowlist secret

    monkeypatch.setenv(
        "AWS_SM_DB_CONFIG_SECRET_ID", "test_db_config_secret_id"
    )  # pragma: allowlist secret

    with patch(
        "botocore.client.BaseClient._make_api_call", new=mock_make_api_call
    ):

        config = AWSSecretsManagerConfig()

        assert (
            config.SQLALCHEMY_DATABASE_URI
            == "postgresql+psycopg2://test_db_user:test_db_password"
            "@test_db_host:5432/"
            "test_db_name?sslmode=verify-full&sslrootcert=test_db_ssl_root_certificate"
        )

        assert config.KEYCLOAK_BASE_URI == "test_keycloak_base_uri"
        assert config.KEYCLOAK_CLIENT_ID == "test_keycloak_client_id"
        assert config.KEYCLOAK_REALM_NAME == "test_keycloack_realm_name"
        assert (
            config.KEYCLOAK_CLIENT_SECRET
            == "test_keycloak_client_secret"  # pragma: allowlist secret
        )
        assert (
            config.SECRET_KEY == "test_secret_key"  # pragma: allowlist secret
        )
        assert config.DEFAULT_PAGE_SIZE == 10
        assert config.DEFAULT_DATE_FORMAT == "test_default_date_format"

        assert config.RECORD_BUCKET_NAME == "test_record_bucket_name"
        assert config.FLASKS3_ACTIVE is False
        assert config.FLASKS3_CDN_DOMAIN == "test_flasks3_cdn_domain"
        assert config.FLASKS3_BUCKET_NAME == "test_flasks3_bucket_name"
        assert config.PERF_TEST is False
        assert config.OPEN_SEARCH_HOST == "test_os_host"
        assert config.OPEN_SEARCH_TIMEOUT == 10

        aws_auth = config.OPEN_SEARCH_HTTP_AUTH
        assert isinstance(aws_auth, AWS4Auth)
        assert aws_auth.access_id == "test_access_key"
        assert aws_auth.region == "test_aws_region"
        assert aws_auth.service == "es"
        assert aws_auth.session_token == "test_token"
        assert (
            aws_auth.signing_key.secret_key
            == "test_secret_key"  # pragma: allowlist secret
        )


@mock_aws
def test_aws_secrets_manager_config_variable_not_set_error(monkeypatch):
    """
    GIVEN AWS secret with secret_ids`AWS_SM_CONFIG_SECRET_ID`,
        `AWS_SM_KEYCLOAK_CLIENT_SECRET_ID` and `AWS_SM_DB_CONFIG_SECRET_ID`
        set and a variable 'DEFAULT_DATE_FORMAT' is not set
    WHEN Config is initialized
    THEN it should raise an exception with error
    """
    secret_value = json.dumps(
        {
            "AWS_REGION": "test_aws_region",
            "KEYCLOAK_BASE_URI": "test_keycloak_base_uri",
            "KEYCLOAK_CLIENT_ID": "test_keycloak_client_id",
            "KEYCLOAK_REALM_NAME": "test_keycloack_realm_name",
            "KEYCLOAK_CLIENT_SECRET": "test_keycloak_client_secret",  # pragma: allowlist secret
            "RECORD_BUCKET_NAME": "test_record_bucket_name",
            "FLASKS3_ACTIVE": "False",
            "FLASKS3_CDN_DOMAIN": "test_flasks3_cdn_domain",
            "PERF_TEST": "False",
            "FLASKS3_BUCKET_NAME": "test_flasks3_bucket_name",
            "SECRET_KEY": "test_secret_key",  # pragma: allowlist secret
            "DB_SSL_ROOT_CERTIFICATE": "test_db_ssl_root_certificate",
            "DEFAULT_PAGE_SIZE": 10,
            "CSP_CONNECT_SRC": "",
            "CSP_DEFAULT_SRC": "",
            "CSP_FRAME_SRC": "",
            "CSP_IMG_SRC": "",
            "CSP_OBJECT_SRC": "",
            "CSP_SCRIPT_SRC": "",
            "CSP_SCRIPT_SRC_ELEM": "",
            "CSP_STYLE_SRC": "",
            "CSP_STYLE_SRC_ELEM": "",
            "CSP_WORKER_SRC": "",
        }
    )

    secret_kc_value = json.dumps({"SECRET": "test_keycloak_client_secret"})

    secret_db_value = json.dumps(
        {
            "username": "test_db_user",
            "password": "test_db_password",  # pragma: allowlist secret
            "port": "5432",
            "proxy": "test_db_host",
            "dbname": "test_db_name",
        }
    )

    ssm_client = boto3.client("secretsmanager")

    ssm_client.create_secret(
        Name="test_secret_id",
        SecretString=secret_value,
    )

    ssm_client.create_secret(
        Name="test_kc_secret_id",
        SecretString=secret_kc_value,
    )

    ssm_client.create_secret(
        Name="test_db_config_secret_id",
        SecretString=secret_db_value,
    )

    monkeypatch.setenv(
        "AWS_SM_CONFIG_SECRET_ID", "test_secret_id"
    )  # pragma: allowlist secret

    monkeypatch.setenv(
        "AWS_SM_KEYCLOAK_CLIENT_SECRET_ID", "test_kc_secret_id"
    )  # pragma: allowlist secret

    monkeypatch.setenv(
        "AWS_SM_DB_CONFIG_SECRET_ID", "test_db_config_secret_id"
    )  # pragma: allowlist secret

    config = AWSSecretsManagerConfig()

    with pytest.raises(KeyError) as error:
        inspect.getmembers(config)

    assert str(error.value) == "'DEFAULT_DATE_FORMAT'"
