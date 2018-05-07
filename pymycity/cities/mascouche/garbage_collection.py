
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature, feature_decorator
from pymycity.item import Item

URL = "https://ville.mascouche.qc.ca/services-aux-citoyens/collectes/"
COLLECT_URL = "https://ville.mascouche.qc.ca/wp-content/themes/mascouche/ajax/tasks.php"

TYPES = (("#a7501c", "compost"),
("#000000", "déchets"),
("#f4e509", "gros rebus"),
("#256bae", "recyclage"),
("#f60000", "rdd"),
("#34af28", "résidus verts"),
)


class GarbageCollection(CityFeature):

    help = "List next garbage collection"
    name = "garbage_collection"

    def _add_arguments(self):
        self.parser.add_argument('-t', '--garbage-type', required=True,
                            choices=[gt[1] for gt in TYPES],
                            help='Collect type')

    @staticmethod
    def _get_garbage_type_color(name):
        for type_ in TYPES:
            if type_[1].lower() == name.lower():
                return type_[0]
        raise Exception("GarbageTypeError")

    async def cli_call(self, cli_args):
        results = await self.call(cli_args.garbage_type,
                                  show_all=cli_args.show_all,
                                  count=cli_args.count)
        print("Next {} collection for {}:".format(cli_args.garbage_type,
                                                  self.city.name.capitalize()))
        for result in results:
            print(result.start.strftime("    * %d %b %Y"))

    @feature_decorator
    async def call(self, garbage_type, show_all=False, count=None):
        item_metadata = self._item_metadata
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
            garbage_color = self._get_garbage_type_color(garbage_type)

            span_nodes = soup.find_all("span", style="background: {}".format(garbage_color))
            for span_node in span_nodes:
                day = span_node.parent.parent.parent.text
                item_metadata["type"] = garbage_type
                
                title = garbage_type
                start = datetime.date(date_.year, date_.month, int(day))
                item = Item(title, start=start, metadata=item_metadata)

                collection_days.append(item)

        return collection_days
