#!/usr/bin/env python
import argparse
import os
import sys
from datadog import initialize
from datadog import api


def cancel_downtime(tags):
    downtimes = api.Downtime.get_all()
    import pprint
    cancel_ids = []
    for d in downtimes:
        if tags in d['scope']:
            cancel_ids.append(d['id'])
    for id in cancel_ids:
        res = api.Downtime.delete(id)
        print(res)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-t", "--tags", help='The dashboard ID', required=True)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    tags = args.tags
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
    if not tags:
        errors.append("""
                      You must supply tags by passing a
                      -t/--tags argument""")
    if errors:
        for error in errors:
            print(error)
        sys.exit(2)
    else:
        # Initialize the dd client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        cancel_downtime(tags)
