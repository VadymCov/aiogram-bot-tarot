import logging, inspect
from typing import TypeVar, Type, Any, cast, Dict

T = TypeVar("T")

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
    _instances: dict[type, Any] = {}

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:

        if cls not in Singleton._instances:
            instance = super().__call__(*args, **kwargs)
            Singleton._instances[cls] = instance

        return Singleton._instances[cls]

class AppLogging(AppLogger, metaclass=Singleton): pass
