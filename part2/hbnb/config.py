import os


class Config:
    """
    Base configuration class containing default settings.
    Can be extended by specific environment configurations.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    Inherits from Config and enables debug mode.
    """
    DEBUG = True


# Dictionary to map environment names to their corresponding config classes
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
