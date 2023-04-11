import datetime
from advert.models import Advert


def desactiveAdvert():
    current_date = datetime.datetime.now().date()
    adverts = Advert.objects.all()
    for advert in adverts:
        if advert.end_date < current_date:
            advert.statut = False
            advert.save()
        else:
            pass
    # print("all poducts are", products)
