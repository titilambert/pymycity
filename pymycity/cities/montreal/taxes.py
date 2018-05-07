
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature, feature_decorator
from pymycity.item import Item

MUNICIPAL_URL="http://ville.montreal.qc.ca/portal/page?_pageid=44,79217&_dad=portal&_schema=PORTAL"

TYPES = ("school", "municipal")

class Taxes(CityFeature):

    help = "List next taxes dates"
    name = "taxes"

    def _add_arguments(self):
        self.parser.add_argument('-t', '--taxe-type', required=True,
                            choices=TYPES,
                            help='Taxe type')

    async def cli_call(self, cli_args):
        results = await self.call(cli_args.taxe_type,
                                  show_all=cli_args.show_all,
                                  count=cli_args.count)
        # print results
        print("Next {} taxes for {}:".format(cli_args.taxe_type,
                                             self.city.name.capitalize()))
        for result in results:
            print(result.start.strftime("    * %d %b %Y"))

    @feature_decorator
    async def call(self, taxe_type):
        item_metadata = self._item_metadata

        taxe_days = []

        if taxe_type == "municipal":
            raw_res = await self._session.get(MUNICIPAL_URL)
            res = await raw_res.text()
            soup = BeautifulSoup(res, 'html.parser')
            li_nodes = soup.find_all("li")   
            for li_node in li_nodes:
                text = li_node.text.strip()
                reg_res = re.match("([A-Za-z]*).([A-Za-z]*).([0-9]*),.([0-9]*)", text)
                if reg_res:
                    day = reg_res.group(3)
                    month = reg_res.group(2)
                    year = reg_res.group(4)
                    start = datetime.datetime.strptime(" ".join((year, month, day)),
                                                             "%Y %B %d").date()
                    title = "taxe municipale"
                    item_metadata["type"] = "municipal"
                    item = Item(title, start=start, metadata=item_metadata)
                    taxe_days.append(item)
        elif taxe_type == "school":
            # TODO
            pass

        return taxe_days
