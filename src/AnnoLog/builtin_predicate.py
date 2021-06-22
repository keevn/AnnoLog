import abc
from AnnoLog.variable import variable


class builtin_predicate(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'filter') and
                callable(subclass.filter) and
                hasattr(subclass, 'reset_df') and
                callable(subclass.reset_df) or
                NotImplemented)

    @abc.abstractmethod
    def filter(self, arguments: [str]) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def reset_df(self):
        raise NotImplementedError

    def __init__(self, arguments: [str]):
        self.arguments = arguments
        self.df = None
        self.reset_df()


class equal(builtin_predicate):
    def __init__(self, arguments: [str]):
        super(equal, self).__init__(arguments)
        if len(self.arguments) != 2:
            raise WrongNumberOfArgumentsError
        self.values = [None] * 2

    def __repr__(self):
        return '='.join(self.values)

    def reset_df(self):
        pass

    def filter(self, resolution) -> dict:
        if isinstance(self.arguments[0], variable):
            self.values[0] = resolution[str(self.arguments[0])]
        else:
            self.values[0] = self.arguments[0]

        if isinstance(self.arguments[1], variable):
            self.values[1] = resolution[str(self.arguments[1])]
        else:
            self.values[1] = self.arguments[1]

        return self.values[0] == self.values[1]


class unequal(builtin_predicate):
    def __init__(self, arguments: [str]):
        super(unequal, self).__init__(arguments)
        if len(self.arguments) != 2:
            raise WrongNumberOfArgumentsError
        self.values = [None] * 2

    def __repr__(self):
        return '!='.join(self.arguments)

    def reset_df(self):
        pass

    def filter(self, resolution) -> dict:
        if isinstance(self.arguments[0], variable):
            self.values[0] = resolution[str(self.arguments[0])]
        else:
            self.values[0] = self.arguments[0]

        if isinstance(self.arguments[1], variable):
            self.values[1] = resolution[str(self.arguments[1])]
        else:
            self.values[1] = self.arguments[1]

        return self.values[0] != self.values[1]


class WrongNumberOfArgumentsError(Exception):
    """Base class for other exceptions"""
    pass
