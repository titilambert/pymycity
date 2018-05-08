import argparse
import aiohttp
import datetime
import importlib
import functools
import os

import aiohttp


class City():

    def __init__(self, parent_subparsers, httpsession=None):
        self.name = self.__class__.__name__.lower()
        self.parser = parent_subparsers.add_parser(self.name)
        self.parser_command = self.parser.add_subparsers(title='Command',
                                                         description='City command',
                                                         dest='command',
                                                         help='City Command',
                                                         )
        self.commands = []
        self._session = httpsession

    def close_session(self):
        """Close current session."""
        if not self._session.closed:
            if self._session._connector_owner:
                self._session._connector.close()
            self._session._connector = None


class CityFeature():

    def __init__(self, city):
        self.city = city
        self.parser = city.parser_command.add_parser(self.name, help=self.help)
        self._add_arguments()
        self._session = city._session
        # Register new methods to the city object
        setattr(city, self.name, self.call)
        setattr(city, "cli_" + self.name, self.cli_call)
        self._item_metadata = {"city": self.city.name,
                                 "feature": self.name,
                                 }

    def _add_arguments(self):
        raise NotImplementedError

    async def _get_aiohttpsession(self):
        if self._session is None:
            self.city._session = aiohttp.ClientSession()
            self._session = self.city._session

    async def cli_call(self):
        raise NotImplementedError

    async def call_(self):
        await self._get_aiohttpsession()
        raise NotImplementedError


def feature_decorator(func):
    def wrapper():

        @functools.wraps(func)
        async def wrapped(obj, *args, show_all=False, count=None, **kwargs):
            # Prepare results
            results = []
            # Set aiohttp session
            if obj._session is None:
                obj.city._session = aiohttp.ClientSession()
                obj._session = obj.city._session
            # Call feature
            func.__globals__['count'] = count
            func.__globals__['show_all'] = show_all

            items = await func(obj, *args, **kwargs)
            # Sort items
            items.sort(key=lambda x: x.start)
            # Keep only next date
            # Get day
            today = datetime.date.today()
            if not show_all:
                for item in items:
                    if isinstance(item.start, datetime.datetime):
                        item_start_date = item.start.date()
                    else:
                        item_start_date = item.start
                    if item_start_date - today > datetime.timedelta(0):
                        results.append(item)
            else:
                results = items
            # Handle count
            if count is not None:
                # Improve count handler
                results = results[:count]
            return results
        return wrapped
    return wrapper()


def list_cities():
    cities = []
    current_folder = os.path.dirname(os.path.realpath(__file__))
    for subfolder in os.listdir(current_folder):
        city_name = subfolder
        city_folder = os.path.join(current_folder, subfolder)
        if subfolder in ("__pycache__", ):
            continue
        elif not os.path.isdir(city_folder):
            continue
        city_init_file = os.path.join(city_folder, "__init__.py")
        if not os.path.isfile(city_init_file):
            continue
        cities.append(city_name)
    return cities


def get_city_module(city_name, subparsers=None, httpsession=None):
    if subparsers is None:
        fakeparser = argparse.ArgumentParser(add_help=False)
        subparsers = fakeparser.add_subparsers()
    city_module = importlib.import_module("pymycity.cities." + city_name)
    city_object = getattr(city_module, city_name.capitalize())(subparsers, httpsession)
    return city_object


def get_supported_cities(subparsers):
    cities = {}
    for city_name in list_cities():
        city_object = get_city_module(city_name, subparsers)
        cities[city_name] = city_object
    return cities
