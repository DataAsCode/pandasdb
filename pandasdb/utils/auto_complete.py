from copy import deepcopy

from pandasdb.utils.misc import string_to_python_attr


class AutoComplete:
    def __init__(self, name, kwargs):
        self.name = name
        self._kwargs = kwargs
        for name, val in kwargs.items():
            setattr(self, string_to_python_attr(name), val)

    def __str__(self):
        return f"{self.name}({', '.join(self._kwargs.keys())})"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        kwargs = deepcopy(self._kwargs)
        kwargs.update(other._kwargs)
        return AutoComplete(self.name, kwargs)

    def __iter__(self):
        return iter(self._kwargs.values())

    def __contains__(self, item):
        if hasattr(item, "name"):
            item = string_to_python_attr(item.name)

        return item in self._kwargs

    def get(self, name):
        try:
            return getattr(self, string_to_python_attr(name))
        except AttributeError:
            raise ValueError(f"{string_to_python_attr(name)} not found in {self.name}")
