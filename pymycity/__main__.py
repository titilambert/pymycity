import asyncio
import argparse
import json
import sys

from pymycity.cities import get_supported_cities
from pymycity.misc import cli_helper

REQUESTS_TIMEOUT = 4


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--timeout',
                        default=REQUESTS_TIMEOUT, help='Request timeout')
    parser.add_argument('-a', '--show-all',
                        action="store_true", default=False,
                        help='Show all (not only the next dates)')
    parser.add_argument('-c', '--count',
                        type=int, default=None,
                        help='Show only N results')
    subparsers = parser.add_subparsers(title='City',
                                       description='Supported Cities',
                                       dest='city',
                                       help='City name')
    # Load all cities
    cities = get_supported_cities(subparsers)
    # Parse args
    cli_args = parser.parse_args()
    if cli_args.city is None:
        cli_helper(parser, cities)
        return
    # Get selected city
    mycity = cities[cli_args.city]
    # Run command
    if cli_args.command is None:
        mycity.parser.print_help()
    else:
        loop = asyncio.get_event_loop()
        city_func = getattr(mycity, "cli_" + cli_args.command)
        fut = asyncio.wait([city_func(cli_args)])
        try:
            loop.run_until_complete(fut)
        except Exception:
            mycity.close_session()
            return
        mycity.close_session()


if __name__ == '__main__':
    sys.exit(main())
