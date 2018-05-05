
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature

MUNICIPAL_URL="https://ville.mascouche.qc.ca/services-aux-citoyens/taxes/"
SCHOOL_URL="https://ville.mascouche.qc.ca/services-aux-citoyens/taxes/"

TYPES = ("school", "municipal")
MONTHS = {"janvier": 1,
          "février": 2,
          "mars": 3,
          "avril": 4,
          "mai": 5,
          "juin": 6,
          "juillet": 7,
          "août": 8,
          "septembre": 9,
          "octobre": 10,
          "novembre": 11,
          "décembre": 12,
          }

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
            #html = json.loads(res.content.decode('utf-8-sig')).get("html")
            soup = BeautifulSoup(res, 'html.parser')
            h1_node = soup.find("h1", text=re.compile("Taxes municipales"))
            li_nodes = h1_node.parent.find_all("li")
            for li_node in li_nodes:
                text = li_node.text.replace("\xa0", " ")
                day_name, day, month, year = text.split(" ")
                re_day_int = re.search(r"[0-9]*", day)
                if not re_day_int.group():
                    raise
                day_int = int(re_day_int.group(0))
                month_int = MONTHS[month]
                year_int = int(year)
                taxe_days.append(datetime.date(year_int, month_int, day_int))
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
