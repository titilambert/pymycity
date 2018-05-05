from pymycity.cities import City
from pymycity.cities.montreal.taxes import Taxes

URL = "http://ville.mascouche.qc.ca"


class Montreal(City):

    language = "fr"
    languages = ["fr", "en"]
    country = "canada"
    province = "québec"
    
    def __init__(self, parent_subparsers, httpsession=None):
        super().__init__(parent_subparsers, httpsession)
        self.commands.append(Taxes(self))
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
