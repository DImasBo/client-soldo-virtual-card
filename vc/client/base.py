from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from vc.db.base_class import Base


class BaseNetworkClient(object):
    _user = None

    def __init__(self, uri: str, pool_timeout=10,
                 pool_size=5, max_overflow=100,
                 connect_timeout=10,
                 session_name="virtual_card", user_model=None, celery_broker=None, celery_backend=None, **kwargs):
        self._user = user_model
        self.engine = create_engine(uri, pool_pre_ping=True,
                                    pool_timeout=pool_timeout,
                                    pool_size=pool_size, max_overflow=max_overflow,
                                    connect_args={'connect_timeout': connect_timeout,
                                                  "application_name": session_name})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    @contextmanager
    def get_session(self):
        session = None
        try:
            session = self.SessionLocal()
            yield session
        except Exception as exc:
            try:
                session.rollback()
            except Exception:
                pass
            raise exc
        finally:
            if session:
                session.close()

    def save_obj(self, db, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def oauth_authorize(self):
        raise NotImplementedError

    def whoami(self):
        raise NotImplementedError

    def user_update(self, id:int, **kwargs):
        raise NotImplementedError

    def create_user(self, db: Session, id: int):
        raise NotImplementedError

    def create_wallet(self, request_timestamp, owner_type, currency, name):
        return NotImplementedError

    def create_card(self, request_timestamp, owner_type, owner_public_id,
                    wallet_id, type, name, emboss_line4, card_label="aff"):
        return NotImplementedError

    def add_item_to_group(self, groupId: str, id: str, type="WALLET"):
        return NotImplementedError

    def run_event(self, event_type, event_name, data):
        return NotImplementedError
