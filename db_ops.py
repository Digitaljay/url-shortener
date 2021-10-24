from models import Url
from sqlalchemy import func


def db_create_url(session, long_url):
    url = Url(long_url=long_url,
              short_url=db_len(session),
              views=0)
    session.add(url)
    session.commit()


def db_read_url_by_long(session, long_url):
    return session.query(Url).filter(Url.long_url == long_url).first()


def db_read_url_by_short(session, short_url):
    return session.query(Url).filter(Url.short_url == short_url).first()


def db_plus_view(session, short_url):
    session.query(Url).filter(Url.short_url == short_url).update({Url.views: Url.views + 1})
    session.commit()


def db_len(session):
    return session.query(func.count(Url.short_url)).scalar()
