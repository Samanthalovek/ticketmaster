from pia import db
from pia.models import Place


def set_image_path(id=1):
    if id == 1:
        return "img/pink.jpg"
    elif id == 2:
        return "img/futbol.jpg"
    else:
        return "img/art.jpg"


def set_images(events):
    for event in events:
        setattr(event, "filename", set_image_path(event.iIdEvento))


def get_place(id):
    place = db.session.query(Place).filter_by(iIdLugar=id).first()
    return f"{place.vPais}, {place.vMunicipio} {place.vEstado}"