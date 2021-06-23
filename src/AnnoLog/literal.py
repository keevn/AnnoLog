import re

import pandas as pd

from AnnoLog.context import context
from AnnoLog.variable import variable


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

    @staticmethod
    def parseLiteral(line):
        constant_name_pattern = re.compile(r'[a-z|$][a-z|\d_]*')
        constant_value_pattern = re.compile(r'[a-z|\d_]*')
        variable_pattern = re.compile(r'[A-Z][A-Z|\d_]*')
        literal_pattern = re.compile(
            r'[\s]*([a-z|$][a-z|\d_]*)[\s]*'
            r'\([\s]*([a-z|A-Z][a-z|A-Z\d_,\s]*)[\s]*\)[\s]*'
            r'(@[\s]*[a-z|A-Z][a-z|A-Z\d_+\s]*)?')
        m = literal_pattern.match(line)
        if m:
            literal_components = list(m.groups())
            if constant_name_pattern.fullmatch(literal_components[0]):
                predicate = literal_components[0].strip()
            else:
                return None
            arguments = literal_components[1].split(',')
            find_match = True
            for i, arg in enumerate(arguments):
                if arg is None or arg == '':
                    find_match = False
                    break
                else:
                    if constant_value_pattern.fullmatch(arg.strip()):
                        arguments[i] = arg.strip()
                    elif variable_pattern.fullmatch(arg.strip()):
                        arguments[i] = variable(arg.strip())
                    else:
                        find_match = False
                        break
            ct = literal_components[-1]
            ct_list = None
            if find_match:
                if ct is not None:
                    ct_list = []
                    ct_name_list = literal_components[-1][1:].strip().split('+')
                    for ct_name in ct_name_list:
                        if ct_name is None or ct_name == '':
                            find_match = False
                            break
                        else:
                            if constant_value_pattern.fullmatch(ct_name.strip()):
                                ct_list.append(context(ct_name.strip()))
                            elif variable_pattern.fullmatch(ct_name.strip()):
                                ct_list.append(context(variable(ct_name.strip())))
                            else:
                                find_match = False
                                break
                if find_match:
                    return literal(predicate, arguments, ct_list)

            return None



