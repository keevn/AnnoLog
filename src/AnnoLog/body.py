import re

import pandas as pd

from AnnoLog.builtin_predicate import *
from AnnoLog.literal import literal


class body:
    def __init__(self, literals: [literal], expressions: [builtin_predicate] = None):
        self.literals = literals
        self.expressions = expressions
        self.resolutions = []

    def unify(self, factList, contextList):
        for li in self.literals:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))
            #li.show()

        new_fact_df = self.literals[0].df

        for i in range(0, len(self.literals) - 1):
            if new_fact_df.empty:
                return
            elif not self.literals[i + 1].df.empty:
                common_variables = list(set(new_fact_df.columns).intersection(set(self.literals[i + 1].df.columns)))
                if len(common_variables) > 0:
                    new_fact_df = pd.merge(new_fact_df, self.literals[i + 1].df, on=common_variables).drop_duplicates() \
                        .reset_index(drop=True)
                else:
                    new_fact_df = new_fact_df.merge(self.literals[i + 1].df, how='cross').drop_duplicates() \
                        .reset_index(drop=True)
            else:
                return
        #print(new_fact_df)

        resolutions = []
        for _, row in new_fact_df.iterrows():
            resolutions.append(row.to_dict())

        self.resolutions = []
        if self.expressions is not None:
            for expression in self.expressions:
                for resolution in resolutions:
                    if expression.filter(resolution):
                        self.resolutions.append(resolution)
        else:
            self.resolutions = resolutions

        return self.resolutions

    def __repr__(self):
        literal_strings = []
        for l in self.literals:
            literal_strings.append(str(l))
        expression_strings = []
        if self.expressions is not None:
            for e in self.expressions:
                expression_strings.append(str(e))
            literal_strings.extend(expression_strings)
        return ','.join(literal_strings)


    @staticmethod
    def parseBody(line):
        constant_value_pattern = re.compile(r'[a-z|\d_]*')
        variable_pattern = re.compile(r'[A-Z][A-Z|\d_]*')
        literal_or_expression_pattern = re.compile(
            r'([\s]*[a-z|$][a-z|\d_]*[\s]*'
            r'\([\s]*[a-z|A-Z][a-z|A-Z\d_,\s]*[\s]*\)[\s]*'
            r'(?:@[\s]*[a-z|A-Z][a-z|A-Z\d_+\s]*)?'
            r'|[\s]*[a-z|A-Z][a-z|A-Z\d_,\s]*[\s]*!?=[\s]*[a-z|A-Z][a-z|A-Z\d_,\s]*[\s]*)')

        expression_pattern = re.compile(
            r'[\s]*([a-z|A-Z][a-z|A-Z\d_,\s]*)[\s]*([!]?=)[\s]*([a-z|A-Z][a-z|A-Z\d_,\s]*)[\s]*')

        find_match = True
        literal_string_list = re.findall(literal_or_expression_pattern, line)
        if line == ','.join(literal_string_list):
            # print(literal_string_list)
            literal_list = []
            expression_list = []
            for literal_string in literal_string_list:
                m = expression_pattern.fullmatch(literal_string.strip())
                if m:
                    expression_components = list(m.groups())
                    if expression_components[1] == '!=':
                        if constant_value_pattern.fullmatch(expression_components[0]):
                            expression_components[0] = expression_components[0]
                        elif variable_pattern.fullmatch(expression_components[0]):
                            expression_components[0] = variable(expression_components[0])
                        else:
                            return None
                        if constant_value_pattern.fullmatch(expression_components[2]):
                            expression_components[2] = expression_components[2]
                        elif variable_pattern.fullmatch(expression_components[2]):
                            expression_components[2] = variable(expression_components[2])
                        else:
                            return None
                        expression_list.append(unequal([expression_components[0], expression_components[2]]))
                    elif expression_components[1] == '=':
                        if constant_value_pattern.fullmatch(expression_components[0]):
                            expression_components[0] = expression_components[0]
                        elif variable_pattern.fullmatch(expression_components[0]):
                            expression_components[0] = variable(expression_components[0])
                        else:
                            return None
                        if constant_value_pattern.fullmatch(expression_components[2]):
                            expression_components[2] = expression_components[2]
                        elif variable_pattern.fullmatch(expression_components[2]):
                            expression_components[2] = variable(expression_components[2])
                        else:
                            return None
                        expression_list.append(equal([expression_components[0], expression_components[2]]))
                    else:
                        return None
                else:
                    li = literal.parseLiteral(literal_string)
                    if li is not None:
                        literal_list.append(li)
                    else:
                        return None

            if len(expression_list) == 0:
                expression_list = None

            return body(literal_list, expression_list)


