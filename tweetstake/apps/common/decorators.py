from typing import Any, Dict
import functools


def singleton_to_logging(cls: Any):
    """
    The singleton pattern in a class. To access externally the singleton object
    of the class that uses this decorator, to use: Classname.<obj_singleton>

    :param cls: class that use of the decorator
    :return: instance of the class that use of the decorator (single instance)
    """

    instances: Dict = {}

    def get_instance() -> Any:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()


def singleton(cls):
    """Use class as singleton."""

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it =  cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls
