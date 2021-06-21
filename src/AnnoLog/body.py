import pandas as pd
from AnnoLog.literal import literal
from AnnoLog.builtin_predicate import *


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
            li.show()

        new_fact_df = self.literals[0].df
        for i in range(0, len(self.literals) - 1):
            if new_fact_df.empty:
                return
            elif not self.literals[i + 1].df.empty:
                common_variables = list(set(new_fact_df.columns).intersection(set(self.body[i + 1].df.columns)))
                new_fact_df = pd.merge(new_fact_df, self.body[i + 1].df, on=common_variables).drop_duplicates() \
                    .reset_index(drop=True)
        print(new_fact_df)

        resolutions = []
        for _, row in new_fact_df.iterrows():
            resolutions.append(row.to_dict())

        self.resolutions =[]
        for expression in self.expressions:
            for resolution in resolutions:
                if expression.filter(resolution) is not None:
                    self.resolutions.append(resolution)

        return self.resolutions


