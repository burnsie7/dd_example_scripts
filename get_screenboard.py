#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
import json
from datadog import initialize
from datadog import api


def get_screenboard(dashid):
    sb = api.Screenboard.get(dashid)
    print(sb)
    filename = 'screenboard_' + str(dashid) + '.json'
    file = open(filename, "w")
    file.write(json.dumps(sb, indent=4, sort_keys=True))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-d", "--dashid", help='The dashboard ID', required=True)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    dashid = args.dashid
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
    if not dashid:
        errors.append("""
                      You must supply a Screenboard id by passing a
                      -d/--dashid argument""")
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
        get_screenboard(dashid)
