from AnnoLog.variable import variable
from AnnoLog.fact import fact
from AnnoLog.context import context
import pandas as pd


class literal:
    def __init__(self, predicate, arguments, ct=None):
        self.predicate = predicate
        self.arguments = arguments
        self.context = ct
        self.data = {}
        self.df = None
        self.reset_df()

    def __repr__(self):
        argumentStr = []
        for arg in self.arguments:
            if isinstance(arg, variable):
                argumentStr.append(str(arg))
            else:
                argumentStr.append(arg)
        return '{predicate}({arguments}){context}'. \
            format(predicate=self.predicate,
                   arguments=','.join(argumentStr),
                   context='' if self.context is None else '@' + str(self.context.name))

    def add_match(self, new_row):
        self.df = self.df.append(new_row, ignore_index=True)

    def reset_df(self):
        self.data = {}
        for arg in self.arguments:
            if isinstance(arg, variable):
                self.data[str(arg)] = []
        if isinstance(self.context, variable):
            self.data[str(self.context)] = []
        self.df = pd.DataFrame(self.data)

    def show(self):
        print(self.df)

    def generate_name_fact(self, resolution):
        arguments = []
        for arg in self.arguments:
            if isinstance(arg, variable):
                arguments.append(resolution[str(arg)])
            else:
                arguments.append(arg)
        if isinstance(self.context.name, variable):
            ct = context(resolution[str(self.context.name)])
        else:
            ct = self.context
        return fact(self.predicate, arguments, ct=ct, genetic=False)

