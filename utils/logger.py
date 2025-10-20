import logging, inspect

class AppLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    @staticmethod
    def get_logger():
        caller = inspect.stack()[1].frame.f_globals.get("__name__", "__main__")
        return logging.getLogger(f"{caller}")


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(cls, *args, **kwargs)
        return cls.instances[cls]


class AppLogging(AppLogger, metaclass=Singleton): pass
