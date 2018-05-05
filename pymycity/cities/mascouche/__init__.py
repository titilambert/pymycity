from pymycity.cities import City
from pymycity.cities.mascouche.garbage_collection import GarbageCollection
from pymycity.cities.mascouche.taxes import Taxes
from pymycity.cities.mascouche.events import Events

URL = "http://ville.mascouche.qc.ca"


class Mascouche(City):

    language = "fr"
    country = "canada"
    province = "québec"
    
    def __init__(self, parent_subparsers, httpsession=None):
        super().__init__(parent_subparsers, httpsession)
        self.commands.append(GarbageCollection(self))
        self.commands.append(Taxes(self))
        self.commands.append(Events(self))
        # TODO
        ## Attr
        # GPS
        # ???
        ## func
        # Garbage
        # Taxes
        # Events (cultural,...)
        # Alert water,...
        # Schools
        # travaux=>English
        # Gas price
        # Trafic
        # ???
