import logging


class AppLogging:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
            )
            handler.setFormater(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(cls, *args, **kwargs)
        return cls.instances[cls]


class AppLogger(AppLogging, metaclass=Singleton): pass
