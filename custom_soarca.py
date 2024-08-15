#!/usr/bin/env python3

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Exit error codes
ERR_NO_REQUEST_MODULE = 1
ERR_BAD_ARGUMENTS = 2
ERR_FILE_NOT_FOUND = 6
ERR_INVALID_JSON = 7

debug_enabled = False
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
alert_json = {}
json_options = {}

LOG_FILE = f'{pwd}/logs/integrations.log'

ALERT_INDEX = 1
API_KEY_INDEX = 2
WEBHOOK_INDEX = 3
PLAYBOOK_ID = 4

CACAO_VAR_TYPE_STRING = "string"
CACAO_VAR_TYPE_INT = "integer"
CACAO_VAR_TYPE_IP4 = "ipv4-addr"

try:
    import requests
except Exception:
    print("No module 'requests' found. Install: pip install requests")
    sys.exit(ERR_NO_REQUEST_MODULE)


def debug(msg: str) -> None:
    """Log the message in the log file with the timestamp, if debug flag
    is enabled

    Parameters
    ----------
    msg : str
        The message to be logged.
    """
    if debug_enabled:
        print(msg)
        with open(LOG_FILE, 'a') as f:
            f.write(msg + '\n')


def build_cacao_variable(type, description,  value) -> str:
    var = {
        "type": type,
        "description": description,
        "value": value,
        "constant": True,
        "external": True
    }

    return var


def execute(alert_file_location, webhook, api_key):
    # Read the alert file
    with open(alert_file_location, 'r') as f:
        alert_json = json.loads(f.read())
        debug(alert_json)

        # Generate request
        headers = {'content-type': 'application/json'}

        data = {}
        data["__rule_id__"] = build_cacao_variable(
            CACAO_VAR_TYPE_INT,
            alert_json['rule']['description'],
            alert_json['rule']['id'])
        data["__rule_level__"] = build_cacao_variable(
            CACAO_VAR_TYPE_INT,
            "rule severity level 1 - 15",
            alert_json['rule']['level'])
        data["__times_fired__"] = build_cacao_variable(
            CACAO_VAR_TYPE_INT,
            "number of times the rile fired",
            alert_json['rule']['firedtimes'])
        data["__affected_agent_name__"] = build_cacao_variable(
            CACAO_VAR_TYPE_STRING,
            "agent name that is affected",
            alert_json['agent']['name'])
        data["__affected_agent_ip__"] = build_cacao_variable(
            CACAO_VAR_TYPE_IP4,
            "agent ip that is affected",
            alert_json['agent']['ip'])
        data["__full_log_message__"] = build_cacao_variable(
            CACAO_VAR_TYPE_STRING,
            "the full log message from wazuh",
            alert_json['full_log'])

        # Send the request
        # debug("before")
        response = requests.post(url=webhook, data=data, headers=headers)
        debug(response)


def main(args):

    # Read configuration parameters

    if len(args) >= 4:
        # Read args
        alert_file_location: str = args[ALERT_INDEX]
        debug(alert_file_location)
        webhook: str = args[WEBHOOK_INDEX]
        api_key = args[API_KEY_INDEX]
        execute(alert_file_location=alert_file_location,
                webhook=webhook, api_key=api_key)
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
