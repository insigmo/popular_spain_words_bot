from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, LargeBinary, SmallInteger, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=True)
    is_bot = Column(Boolean, default=False)
    language_code = Column(String(20))
    is_premium = Column(Boolean, default=False, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)
    words_count = Column(SmallInteger, default=10)
    what_hour = Column(SmallInteger, default=10)


class KnownWords(Base):
    __tablename__ = 'known_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), unique=True)
    words = Column(LargeBinary, nullable=False)
