import os
import json

settings = None


class Settings(object):
    """Simple singleton class for managing and accessing settings"""

    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')) as f:
            settings = json.load(f)
            self.url = settings['url']
            self.browser = settings['browser']
            self.driver_timeout = int(settings['driver_timeout'])
            self.role = settings['role']


settings = Settings()
