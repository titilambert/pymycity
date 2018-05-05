
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature

URL = "https://ville.mascouche.qc.ca/services-aux-citoyens/collectes/"
COLLECT_URL = "https://ville.mascouche.qc.ca/wp-content/themes/mascouche/ajax/tasks.php"

TYPES = (("#a7501c", "compost"),
("#000000", "waste"),
("#f4e509", "bulky"),
("#256bae", "recycling"),
("#f60000", "hazardous"),
("#34af28", "organic"),
)


class GarbageCollection(CityFeature):

    help = "List next garbage collection"
    name = "garbage_collection"

    def _add_arguments(self):
        self.parser.add_argument('-t', '--collection-type', required=True,
                            choices=[gt[1] for gt in TYPES],
                            help='Collect type')
        self.parser.add_argument('-n', '--only-next',
                            action="store_true", default=False,
                            help='Show only the next collect')

    @staticmethod
    def _get_garbage_type_color(name):
        for type_ in TYPES:
            if type_[1].lower() == name.lower():
                return type_[0]
        raise Exception("GarbageTypeError")

    async def cli_call(self, cli_args):
        results = await self.call(cli_args.type, cli_args.only_next)
        # print results
        print("Next {} collection for {}:".format(cli_args.type,
                                                  self.city.name.capitalize()))
        for result in results:
            print(result.strftime("    * %d %b %Y"))

    async def call(self, collection_type, only_next=False):
        await self._get_aiohttpsession()
        # Get day
        today = datetime.date.today()
        next_month = today + relativedelta.relativedelta(months=1)

        collection_days = []

        for date_ in (today, next_month):
            data = {
                "task": "getCalendarCollecte",
                "month": date_.strftime("%m"),
                "year": date_.strftime("%Y"),
            }
            res = await self._session.post(COLLECT_URL, data=data)
            raw_res = await res.text()
            html = json.loads(raw_res).get("html")

            soup = BeautifulSoup(html, 'html.parser')
            garbage_color = self._get_garbage_type_color(collection_type)

            span_nodes = soup.find_all("span", style="background: {}".format(garbage_color))
            for span_node in span_nodes:
                day = span_node.parent.parent.parent.text
                collection_days.append(datetime.date(date_.year, date_.month, int(day)))

        # Compare
        if only_next:
            for collection_day in collection_days:
                if collection_day - today > datetime.timedelta(0):
                    return [collection_day]
            raise Exception("Not collection found")
            return []
        return sorted(collection_days)
