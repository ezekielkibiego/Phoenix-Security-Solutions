class Config:
    pass


class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kevson:Antidolofinomonoligasta102@localhost/phoenixdb'


class ProdConfig(Config):
    pass

config_options = {
    'development' : DevConfig,
    'production': ProdConfig
}