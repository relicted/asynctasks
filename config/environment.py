import os

ENVIRONMENT = os.getenv('ENV', 'development')

if ENVIRONMENT == 'development':
    SETTINGS_FILE = 'config.settings.development'
elif ENVIRONMENT == 'production':
    SETTINGS_FILE = 'config.settings.production'
else:
    SETTINGS_FILE = 'config.settings.development'
