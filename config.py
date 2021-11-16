import os
class Config:
    SECRET_KEY = os.environ.get('SECRETE_KEY')


class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kevson:Antidolofinomonoligasta102@localhost/phoenixdb'


class ProdConfig(Config):
    pass

config_options = {
    'development' : DevConfig,
    'production': ProdConfig
}