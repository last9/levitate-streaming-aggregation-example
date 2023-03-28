import requests
import json
import argparse
from requests.auth import HTTPBasicAuth
import os

APP_URL = "https://app.last9.io/api"
ACCESS_TOKEN_PATH = "/v4/oauth/access_token"
CONFIG_PATH = "config.json"
UPDATE_PATH = "/v2/leveetate/org/{tenant}/v1/mgmt/tenant/{tenant}/clusters/{cluster_id}/events/sap"
VALIDATE_PATH = "/v2/leveetate/org/{tenant}/v1/mgmt/tenant/{tenant}/clusters/{cluster_id}/events/validate_sap"
TOKEN_HEADER = "X-LAST9-API-TOKEN"
PIPELINES_PATH = os.environ.get("PIPELINES_PATH", ".")

def get_access_token(token_type):
    refresh_token = os.environ.get("{}_REFRESH_TOKEN".format(token_type.upper()))
    if not refresh_token:
        raise Exception("REFRESH_TOKEN not found in environment")
    r = requests.post(
        APP_URL + ACCESS_TOKEN_PATH,
        json={
            "refresh_token": refresh_token,
        },
    )
    if r.status_code != 200:
        raise Exception(f"Failed to get access token: {r.text}")
    r.raise_for_status()
    return r.json()["access_token"]

def doit(action, config):
    tenant = config["tenant"]
    if not tenant:
        raise Exception("Tenant not found in config")

    ret = []
    for cluster, config in config["clusters"].items():
        yaml_file = os.path.join(PIPELINES_PATH, cluster + ".yaml")
        with open(yaml_file) as f:
            yaml = f.read()
        if action == "update":
            path = UPDATE_PATH.format(
                tenant=tenant, cluster_id=config["cluster_id"]
            )
        elif action == "validate":
            path = VALIDATE_PATH.format(
                tenant=tenant, cluster_id=config["cluster_id"]
            )
        url = APP_URL + path
        r = requests.post(
            url,
            data=yaml,
            headers={
                "region": config["region"],
                "tenant": tenant,
                TOKEN_HEADER: "Bearer {}".format(get_access_token("write")),
            },
        )

        if r.status_code > 201:
            ret.append((cluster, r.text))
    if ret:
        print(f"{action} failed for the following clusters:")
        for cluster, error in ret:
            print(cluster, error)
        exit(1)
    else:
        print(f"{action} successful")

def get_sap(config):
    tenant = config["tenant"]
    if not tenant:
        raise Exception("Tenant not found in config")

    for cluster, config in config["clusters"].items():
        path = UPDATE_PATH.format(
            tenant=tenant, cluster_id=config["cluster_id"]
        )
        url = APP_URL + path
        r = requests.get(
            url,
            headers={
                "region": config["region"],
                "tenant": tenant,
                TOKEN_HEADER: "Bearer {}".format(get_access_token("read")),
            },
        )
        if r.status_code != 200:
            print(f"Failed to get SAP for {cluster}")
        else:
            print(f"SAP for {cluster}:")
            print(r.text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["update", "validate", "get"])
    parser.add_argument("--config") # , default=CONFIG_PATH)
    args = parser.parse_args()
    with open(args.config) as f:
        config = json.load(f)
    if args.action == "get":
        get_sap(config)
        return
    doit(args.action, config)

if __name__ == "__main__":
    main()
