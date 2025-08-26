import os
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # if we just need to use SQLite, just use the below:
    SQLALCHEMY_DATABASE_URI = "sqlite:///{dir}//{dbname}.db".format(dir=basedir, dbname=os.environ.get("POSTGRES_DB"))

    # dialect to connect to postgresql database:
    # dialect+driver://username:password@host:port/database_name

    # PostgreSQL_username = os.environ.get('POSTGRESQL_USERNAME')
    # PostgreSQL_password = urllib.parse.quote_plus(str(os.environ.get('POSTGRESQL_PASSWORD')))
    # PostgreSQL_host = os.environ.get('POSTGRESQL_HOST')
    # PostgreSQL_port = os.environ.get('POSTGRESQL_PORT')
    # PostgreSQL_db = os.environ.get('POSTGRESQL_DB')
    # PostgreSQL_args = os.environ.get('POSTGRESQL_ARGS')
    #
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database_name}?{args}'.format(
    #     user=PostgreSQL_username,
    #     password=PostgreSQL_password,
    #     hostname=PostgreSQL_host,
    #     port=PostgreSQL_port,
    #     database_name=PostgreSQL_db,
    #     args=PostgreSQL_args
    # )
