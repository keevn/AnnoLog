import abc


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
    def reset_df(self):
        pass

    def filter(self, resolution) -> dict:
        pass


class unequal(builtin_predicate):
    def reset_df(self):
        pass

    def filter(self, resolution) -> dict:
        pass
