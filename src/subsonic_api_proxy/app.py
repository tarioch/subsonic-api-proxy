#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import logging
from flask import Flask, request
import requests


from subsonic_api_proxy import __version__

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="subsonic-api-proxy")
    parser.add_argument(
        '--version',
        action='version',
        version='subsonic-api-proxy {ver}'.format(ver=__version__))
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO")
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    parser.add_argument(
        '-t',
        '--target',
        dest='target',
        help="target subsonic url to call",
        required=True,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """

    args = parse_args(args)
    setup_logging(args.loglevel)
    app.config['target'] = args.target
    app.run(host="0.0.0.0")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()


app = Flask(__name__)


@app.route('/rest/<operation>')
def call(operation):
    target = app.config['target']
    args = request.args

    if operation == 'getPlaylist' and args.get('f', 'xml') == 'json':
        resp = requests.get(f'{target}/rest/{operation}', params=args)
        data = resp.json()

        songList = data['subsonic-response']['playlist']['entry']
        strippedSongList = [{'id': s['id']} for s in songList]
        data['subsonic-response']['playlist']['entry'] = strippedSongList

        responseHeaders = {'Content-Type': 'application/json;charset=UTF-8'}

        return data, resp.status_code, responseHeaders
    else:
        resp = requests.get(
            f'{target}/rest/{operation}', stream=True, params=args)

        return resp.raw.read(), resp.status_code, resp.headers.items()
