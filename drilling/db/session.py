# coding: utf-8

import logging
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import scoped_session

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from functools import wraps


class Model(object):
    """Baseclass for custom user models."""

    #: the query class used.  The :attr:`query` attribute is an instance
    #: of this class.  By default a :class:`BaseQuery` is used.
    # query_class = BaseQuery

    #: an instance of :attr:`query_class`.  Can be used to query the
    #: database for instances of this model.
    pass


class _BoundDeclarativeMeta(DeclarativeMeta):
    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key


def make_declarative_base():
    """Creates the declarative base."""
    base = declarative_base(cls=Model, name='Model', metaclass=_BoundDeclarativeMeta)
    return base


Base = make_declarative_base()


def _create_engine(user, password, host, port, db, pool_recycle=60, charset='utf8'):
    engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % (
        user, password,
        host, port,
        db),
                           pool_size=10,
                           max_overflow=-1,
                           pool_recycle=pool_recycle)
    return engine


def get_engine(bind, engines):
    if not bind or bind not in engines:
        bind = "default"

    return engines.get(bind)


def get_tables_for_bind(bind=None):
    """Returns a list of all tables relevant for a bind."""
    result = []
    # for table in Base.metadata.tables.itervalues():
    for table in Base.metadata.tables.values():
        if table.info.get('bind_key') == bind:
            result.append(table)
    return result


def get_binds(engines):
    """Returns a dictionary with a table->engine mapping. """
    binds = [None] + list(engines or ())
    # print "get_binds", binds
    ret_val = {}
    for bind in binds:
        engine = get_engine(bind, engines)
        tables = get_tables_for_bind(bind)
        ret_val.update(dict((table, engine) for table in tables))
    # print "ret_val", len(ret_val)
    return ret_val


class SignallingSession(SessionBase):
    """The signalling session is the default session that Flask-SQLAlchemy
    uses.  It extends the default session system with bind selection and
    modification tracking.

    If you want to use a different session you can override the
    :meth:`SQLAlchemy.create_session` function.

    .. versionadded:: 2.0

    .. versionadded:: 2.1
        The `binds` option was added, which allows a session to be joined
        to an external transaction.
    """

    def __init__(self, **options):
        self.binds = {}
        self.engines = {}
        if "engines" in options:
            self.engines = options.get("engines")
            options.pop("engines")

        if "binds" not in options and self.engines:
            self.binds = get_binds(self.engines)
            options["binds"] = self.binds

        super(SignallingSession, self).__init__(**options)

    def set_binds(self, binds):
        if binds is not None:
            for mapperortable, bind in binds.items():
                if isinstance(mapperortable, (type, Mapper)):
                    self.bind_mapper(mapperortable, bind)
                else:
                    self.bind_table(mapperortable, bind)

    def query(self, *entities, **kwargs):
        """Return a new :class:`.Query` object corresponding to this
        :class:`.Session`."""
        if not self.binds and self.engines:
            self.binds = get_binds(self.engines)
            if self.binds:
                self.set_binds(self.binds)

        return super(SignallingSession, self).query(*entities, **kwargs)

    def get_bind(self, mapper=None, clause=None):
        return super(SignallingSession, self).get_bind(mapper, clause)


OilSession = scoped_session(sessionmaker(class_=SignallingSession))


def _is_session_bind(session):
    return session.session_factory.kw.get('bind') and session.session_factory.kw.get('engines')


def config_oil_session(conf, pool_recycle=60):
    if _is_session_bind(OilSession):
        logging.warning("config_oil_session oil_session is bind already.")

    engine = _create_engine(conf.smart_screen_user, conf.smart_screen_password, conf.smart_screen_host,
                            int(conf.smart_screen_port), conf.smart_screen_name, pool_recycle=pool_recycle, )
    from multiprocessing.util import register_after_fork
    register_after_fork(engine, engine.dispose())
    engines = {'utf8mb4': engine, 'default': engine}
    OilSession.configure(bind=engine, engines=engines, autocommit=False, autoflush=False, expire_on_commit=False)


def with_session(func):
    @wraps(func)
    def _wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        OilSession.remove()
        return response

    return _wrapped
