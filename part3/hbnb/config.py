import os


class Config:
    """
    Base configuration class containing default settings.
    Can be extended by specific environment configurations.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    Inherits from Config and enables debug mode.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Dictionary to map environment names to their corresponding config classes
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
