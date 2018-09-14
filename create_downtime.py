#!/usr/bin/env python
import argparse
import time
import os
import sys
from datadog import initialize
from datadog import api


def create_downtime(tags):
    # Repeat for 3 hours (starting now) on every week day for 4 weeks.
    start_ts = int(time.time())
    end_ts = start_ts + (3 * 60 * 60)
    end_reccurrence_ts = start_ts + (4 * 7 * 24 * 60 * 60)  # 4 weeks from now

    recurrence = {
        'type': 'weeks',
        'period': 1,
        'week_days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'until_date': end_reccurrence_ts
        }

    res = api.Downtime.create(
        scope=tags,
        start=start_ts,
        end=end_ts,
        recurrence=recurrence)
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
            print textwrap.dedent(error)
        sys.exit(2)
    else:
        # Initialize the dd client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        create_downtime(tags)
