import json
import os

import boto3

from configs.base_config import BaseConfig

# use only for local development
if os.environ.get("DEFAULT_AWS_PROFILE"):
    boto3.setup_default_session(
        profile_name=os.environ.get("DEFAULT_AWS_PROFILE")
    )


class AWSSecretsManagerConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__()
        self.secrets_dict = self._get_secrets_manager_config_dict()

    def _get_secrets_manager_config_dict(self):
        """
        Get string value of `secret_name` in Secrets Manager.
        :param key: Name of key whose value will be returned.
        :return: String value of requested Parameter Store key.
        """
        client = boto3.client(
            service_name="secretsmanager",
        )

        secret_value_json_string = client.get_secret_value(
            SecretId="ayr-test-one-vars"  # pragma: allowlist secret
        )["SecretString"]
        secrets_dict = json.loads(secret_value_json_string)

        return secrets_dict

    @property
    def DB_PASSWORD(self):
        client = boto3.client("rds")
        token = client.generate_db_auth_token(
            DBHostname=self.DB_HOST,
            Port=self.DB_PORT,
            DBUsername=self.DB_USER,
            Region=self.AWS_REGION,
        )
        return token

    def _get_config_value(self, variable_name):
        return self.secrets_dict[variable_name]