from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# писания пусти для тестового файла .env
# load_dotenv(dotenv_path=C:/Users/Egor_yrm/PycharmProjects/apts_mail_exam/.tests.env)
load_dotenv()
# Обьявление переменных для баззы данных
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Base = declarative_base()
db_session = sessionmaker(bind=engine)
session = db_session()


class Email(Base):
    __tablename__ = 'email'
    id_email: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
    recent_changes_data: Mapped[str] = mapped_column()


class Deal(Base):
    __tablename__ = 'deal'
    id_deal: Mapped[int] = mapped_column(primary_key=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
