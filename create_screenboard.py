#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
import json
from datadog import initialize
from datadog import api


def create_screenboard(filename):
    with open(filename) as data_file:
        dash_dict = json.load(data_file)
        title = dash_dict.get('board_title', 'New Screenboard')
        description = dash_dict.get('description', '')
        widgets = dash_dict.get('widgets', [])
        width = dash_dict.get('width', 1024)
        template_variables = dash_dict.get('template_variables', [])
        res = api.Screenboard.create(board_title=title, description=description,
                                     widgets=widgets, template_variables=template_variables, width=width)
        print(res)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-f", "--filename", help='The dashboard ID', required=True)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    filename = args.filename
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
    if not filename:
        errors.append("""
                      You must supply a Screenboard file by passing a
                      -f/--filename argument""")
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
        create_screenboard(filename)
