#!/usr/bin/env python
import argparse
import os
import sys
import json
from datadog import initialize
from datadog import api


def create_timeboard(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        dash_dict = data['dash']
        title = dash_dict.get('title', 'New Timeboard')
        read_only = dash_dict.get('read_only', 'False')
        description = dash_dict.get('description', '')
        temp_graphs = dash_dict.get('graphs', [])
        graphs = []
        for g in temp_graphs:
            if 'viz' not in g['definition']:
                g['definition']['viz'] = "timeseries"
            if g['definition']['viz'] not in ["timeseries","hostmap","distribution","heatmap"]:
                print('skipping graph type: {}'.format(g['definition']['viz']))
                pass
            else:
                graphs.append(g)
        template_variables = dash_dict.get('template_variables', [])
        res = api.Timeboard.create(title=title, description=description, graphs=graphs,
                                   template_variables=template_variables, read_only=read_only)
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
            print(error)
        sys.exit(2)
    else:
        # Initialize the dd client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        create_timeboard(filename)
