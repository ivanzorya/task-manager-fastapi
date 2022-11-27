import databases
import sqlalchemy
from config import Settings
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

settings = Settings()


DB_NAME = settings.db_name
POSTGRES_USER = settings.postgres_user
POSTGRES_PASSWORD = settings.postgres_password
DB_HOST = settings.db_host

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/{DB_NAME}"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "task",
    metadata,
    sqlalchemy.Column("uuid", UUID, primary_key=True),
    sqlalchemy.Column("user_uuid", UUID, sqlalchemy.ForeignKey("user.uuid")),
    sqlalchemy.Column("subject", sqlalchemy.String),
    sqlalchemy.Column("done", sqlalchemy.Boolean),
)

users = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("uuid", UUID, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


Base = declarative_base()
