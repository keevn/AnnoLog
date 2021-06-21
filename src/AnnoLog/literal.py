from AnnoLog.variable import variable
import pandas as pd


class literal:
    def __init__(self, predicate: str, arguments: [], ct: [] = None):
        self.predicate = predicate
        self.arguments = arguments
        self.context = ct

        self.df = None
        self.reset_df()

    def __repr__(self):
        argumentStr = []
        for arg in self.arguments:
            if isinstance(arg, variable): # variable
                argumentStr.append(str(arg))
            else:
                argumentStr.append(arg)  # constance

        context_str = []
        if self.context is not None:
            for ct in self.context:
                if isinstance(ct.name, variable):
                    context_str.append(ct.name.varName)
                else:
                    context_str.append(ct.name)
        return '{predicate}({arguments}){context}'. \
            format(predicate=self.predicate,
                   arguments=','.join(argumentStr),
                   context='' if self.context is None else '@' + '+'.join(context_str))

    def add_match(self, new_row):
        self.df = self.df.append(new_row, ignore_index=True).drop_duplicates()

    def reset_df(self):
        data = {}
        for arg in self.arguments:
            if isinstance(arg, variable):
                data[str(arg)] = []
        if isinstance(self.context, variable):
            data[str(self.context)] = []
        self.df = pd.DataFrame(data)

    def show(self):
        print(self.df)



