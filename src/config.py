"""
Module containing environment configurations
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Development:
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PG_USER = os.environ.get('POSTGRES_USER')
    PG_PASS = os.environ.get('POSTGRES_PASSWORD')
    PG_DB = os.environ.get('POSTGRES_DB')
    PG_HOST = os.environ.get('POSTGRES_HOST')
    PG_PORT = os.environ.get('POSTGRES_PORT')
    PG_SERVICE_NAME = os.environ.get('PG_SERVICE_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@localhost:5432/{PG_DB}'
    print("PG_USER Dev", PG_USER)
    print("SQLALCHEMY_DATABASE_URI Dev: ", SQLALCHEMY_DATABASE_URI)

class Production:
    """
    Production environment configuration
    """
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PG_USER = os.environ.get('POSTGRES_USER')
    PG_PASS = os.environ.get('POSTGRES_PASSWORD')
    PG_DB = os.environ.get('POSTGRES_DB')
    PG_HOST = os.environ.get('POSTGRES_HOST')
    PG_PORT = os.environ.get('POSTGRES_PORT')
    PG_SERVICE_NAME = os.environ.get('PG_SERVICE_NAME')
    #SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@postgres:5432/postgres'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_SERVICE_NAME}:{PG_PORT}/{PG_DB}'

    print("PG_USER", PG_USER)
    print("SQLALCHEMY_DATABASE_URI: ", SQLALCHEMY_DATABASE_URI)


app_config = {
    'development': Development,
    'production': Production,
}
