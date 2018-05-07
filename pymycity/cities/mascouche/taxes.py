
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature, feature_decorator
from pymycity.item import Item

MUNICIPAL_URL="https://ville.mascouche.qc.ca/services-aux-citoyens/taxes/"
SCHOOL_URL="https://ville.mascouche.qc.ca/services-aux-citoyens/taxes/"

TYPES = ("scolaire", "municipale")
# Remove this and use i18n
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
    async def call(self, taxe_type, show_all=False, count=None):
        item_metadata = self._item_metadata
        # Get day
        today = datetime.date.today()
        next_month = today + relativedelta.relativedelta(months=1)

        taxe_days = []

        if taxe_type == "municipale":
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
                start = datetime.date(year_int, month_int, day_int)
                item_metadata["type"] = "municipale"
                title = "taxe municipale"
                item = Item(title=title, start=start, metadata=item_metadata)
                taxe_days.append(item)
        elif taxe_type == "school":
            pass

        return taxe_days
