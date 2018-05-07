
import re
import datetime
from dateutil import relativedelta
import json

from bs4 import BeautifulSoup

from pymycity.cities import CityFeature, feature_decorator
from pymycity.item import Item

URL = "https://ville.mascouche.qc.ca/services-aux-citoyens/calendrier/page/"

TYPES = (("Bibliothèque", 28),
         ("Conseil municipal", 30),
         ("Consultation publique", 129),
         ("Événement", 55),
         ("Formation", 58),
         )
LOCATIONS = (("Bibliothèque Bernard-Patenaude", 10),
             ("Carrefour familial des Moulins", 89),
             ("Chez-Nous du Communautaire", 88),
             ("École Le Prélude", 64),
             ("Église Saint-Henri-de-Mascouche", 76),
             ("Garage municipal", 71),
             ("Noyau villageois (Vieux-Mascouche)", 125),
             ("Parc du Grand-Coteau", 3),
             ("Pavillon du Grand-Coteau", 15),
             ("Salle du conseil municipal", 43),
             ("Théâtre du Vieux-Terrebonne", 128),
             )
CUSTOMERS = (("Adolescent (11 ans et plus)", 90),
            ("Adolescent (9 à 13 ans)", 91),
            ("adolescents", 119),
            ("Adultes", 36),
            ("Aînés", 37),
            ("Enfant 18 à 36 mois", 102),
            ("Enfant 2 à 7 ans", 115),
            ("Enfant 4 à 7 ans", 112),
            ("Enfant 6 à 8 ans", 114),
            ("Enfant 8 à 12 ans", 116),
            ("Jeunes 3 à 5 ans", 101),
            ("Pour tous", 32),
            )

class Events(CityFeature):

    help = "List next city events"
    name = "events"

    def _add_arguments(self):
        self.parser.add_argument('-t', '--event_type', required=False,
                            choices=[et[0] for et in TYPES],
                            help='Event type')
        self.parser.add_argument('-l', '--location', required=False,
                            choices=[l[0] for l in LOCATIONS],
                            help='Event location')
        self.parser.add_argument('-c', '--customer', required=False,
                            choices=[c[0] for c in CUSTOMERS],
                            help='Event customers')
        self.parser.add_argument('-n', '--only-next',
                            action="store_true", default=False,
                            help='Show only the next collect')

    async def cli_call(self, cli_args):
        results = await self.call(cli_args.event_type, cli_args.location, cli_args.customer,
                                  show_all=cli_args.show_all,
                                  count=cli_args.count)
        # print results
        event_type = "all"
        if cli_args.event_type is not None:
            event_type = cli_args.event_type
        print("Next {} events for {}:".format(event_type,
                                              self.city.name.capitalize()))
        for result in results:
            print("")
            print("    {}".format(result.title))
            print("    Date: {}".format(result.start))
            print("    Location: {}".format(result.location))
            print("    URL: {}".format(result.url))

    @feature_decorator
    async def call(self, event_type=None, event_location=None, event_customer=None):
        item_metadata = self._item_metadata
        # Get count param
        _count = globals().get('count')
        if _count is None:
            _count = 5
        # Prepare
        event_list = []
        params = {}
        if dict(TYPES).get(event_type):
            params["activity"] = dict(TYPES).get(event_type)
        if dict(LOCATIONS).get(event_location):
            params["place"] = dict(LOCATIONS).get(event_location)
        if dict(CUSTOMERS).get(event_customer):
            params["customer"] = dict(CUSTOMERS).get(event_customer)

        # TODO launch requests in the "same time"
        for page in range(1, (_count // 6 + 2)):
            event_url = URL + str(page)
            raw_res = await self._session.get(url=event_url, params=params)
            html = await raw_res.text()
            soup = BeautifulSoup(html, 'html.parser')
            ul_node = soup.find("ul", class_="list-events")
            event_nodes = ul_node.find_all("div", class_="entry-info")
            for event_node in event_nodes:
                event_subnode = event_node.find("ul", "entry-link")
                event = {}
                # Get attributes
                ## Title
                title = event_subnode.find("var", class_="atc_title").text
                ## Date start
                raw_data = event_subnode.find("var", class_="atc_date_start").text
                date_start = datetime.datetime.strptime(raw_data, "%Y-%m-%d %H:%M:%S")
                ## Date end
                raw_data = event_subnode.find("var", class_="atc_date_end").text
                date_end = datetime.datetime.strptime(raw_data, "%Y-%m-%d %H:%M:%S")
                ## Description
                description = event_subnode.find("var", class_="atc_description").text
                ## Location
                location = event_subnode.find("var", class_="atc_location").text
                ## Url
                event_node.find("ul", "entry-link").find("li").find("a").attrs.get('href')
                url = ""
                first_li_node = event_node.find("ul", "entry-link").find("li")
                if first_li_node.find("a"):
                    url = first_li_node.find("a").attrs.get('href')
                ## metadata
                # Create object
                item = Item(title,
                            start=date_start,
                            end=date_end,
                            location=location,
                            url=url,
                            description=description,
                            metadata=item_metadata)
                # Add item
                event_list.append(item)

        return event_list
