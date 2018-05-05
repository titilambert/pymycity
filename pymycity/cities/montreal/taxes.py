
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature

MUNICIPAL_URL="http://ville.montreal.qc.ca/portal/page?_pageid=44,79217&_dad=portal&_schema=PORTAL"

TYPES = ("school", "municipal")

class Taxes(CityFeature):

    help = "List next taxes dates"
    name = "taxes"

    def _add_arguments(self):
        self.parser.add_argument('-t', '--type', required=True,
                            choices=TYPES,
                            help='Taxe type')
        self.parser.add_argument('-n', '--only-next',
                            action="store_true", default=False,
                            help='Show only the next dates')
        self.parser.add_argument('-c', '--count',
                            type=int, default=None,
                            help='Show only N results')

    async def cli_call(self, cli_args):
        results = await self.call(cli_args.type, cli_args.only_next, cli_args.count)
        # print results
        print("Next {} taxes for {}:".format(cli_args.type,
                                             self.city.name.capitalize()))
        for result in results:
            print(result.strftime("    * %d %b %Y"))

    async def call(self, taxe_type, only_next=False, count=None):
        await self._get_aiohttpsession()
        # Get day
        today = datetime.date.today()
        next_month = today + relativedelta.relativedelta(months=1)

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
                    tmpdatetime = datetime.datetime.strptime(" ".join((year, month, day)),
                                                             "%Y %B %d")
                    taxe_days.append(tmpdatetime.date())
        elif taxe_type == "school":
            pass

        # Prepare output
        results = []
        # Sort result
        taxe_days.sort()
        # Keep only next date
        if only_next:
            for taxe_day in taxe_days:
                if taxe_day - today > datetime.timedelta(0):
                    results.append(taxe_day)
        else:
            results = taxe_days
        # Handle count
        if count is not None:
            # Improve count handler
            results = results[:count]
        # return
        return results
