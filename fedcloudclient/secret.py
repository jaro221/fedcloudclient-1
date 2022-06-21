"""
Implementation of "fedcloud secret" commands for accessing secret management service
"""

import click
import hvac

from tabulate import tabulate

from fedcloudclient.checkin import get_checkin_id
from fedcloudclient.decorators import oidc_params

VAULT_ADDR = "https://vault.services.fedcloud.eu:8200"
VAULT_ROLE = "demo"
VAULT_MOUNT_POINT = "/secrets"


def secret_client(access_token, command, path, data):
    """
    Client function for accessing secrets
    :param path: path to secret
    :param access_token: access token for authentication
    :param command: the command to perform
    :param data: input data
    :return: Output data from the service
    """

    client = hvac.Client(url=VAULT_ADDR)
    client.auth.jwt.jwt_login(role=VAULT_ROLE, jwt=access_token)
    checkin_id = get_checkin_id(access_token)
    full_path = checkin_id + "/" + path
    function_list = {
        "list_secrets": client.secrets.kv.v1.list_secrets,
        "read_secret": client.secrets.kv.v1.read_secret,
        "delete_secret": client.secrets.kv.v1.read_secret,
    }
    if command == "set":
        response = client.secrets.kv.v1.create_or_update_secret(
            path=full_path,
            mount_point=VAULT_MOUNT_POINT,
            secret=data,
        )
    else:
        response = function_list[command](path=full_path, mount_point=VAULT_MOUNT_POINT)
    return response


@click.group()
def secret():
    """
    Commands for accessing secrets
    """


@secret.command()
@oidc_params
@click.argument("short_path")
def get(
    access_token,
    short_path,
):
    """
    Get a secret from the path
    """

    data = secret_client(access_token, "read_secret", short_path, None)
    print(tabulate(data["data"].items(), headers=["key", "value"]))


@secret.command("list")
@oidc_params
@click.argument("short_path", required=False, default="")
def list_(
    access_token,
    short_path,
):
    """
    List secrets in the path
    """

    data = secret_client(access_token, "list_secrets", short_path, None)
    print("\n".join(map(str, data["data"]["keys"])))
