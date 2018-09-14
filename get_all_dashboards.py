#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
import json
from datadog import initialize
from datadog import api


def get_all_dashboards():
    sbs = api.Screenboard.get_all()['screenboards']
    for sb in sbs:
        id = sb['id']
        filename = 'screenboard_' + str(id) + '.json'
        file = open(filename, "w")
        file.write(json.dumps(api.Screenboard.get(id), indent=4, sort_keys=True))
        file.close()
    tbs = api.Timeboard.get_all()['dashes']
    for tb in tbs:
        id = tb['id']
        filename = 'timeboard_' + str(id) + '.json'
        file = open(filename, "w")
        file.write(json.dumps(api.Timeboard.get(id), indent=4, sort_keys=True))
        file.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    errors = []
    if not api_key:
        errors.append("""
                      You must supply your Datadog API key by either passing a
                      -k/--apikey argument or defining a DD_API_KEY environment
                      variable.""")
    if not app_key:
        errors.append("""
                      You must supply your Datadog application key by either
                      passing a -a/--appkey argument or defining a DD_APP_KEY
                      environment variable.""")
    if errors:
        for error in errors:
            print textwrap.dedent(error)
        sys.exit(2)
    else:
        # Initialize the dd client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        get_all_dashboards()
