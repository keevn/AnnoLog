import pandas as pd
from AnnoLog.head import head
from AnnoLog.fact import fact
from AnnoLog.context import context


class rule:
    def __init__(self, h: head, body):
        self.head = h
        self.body = body
        self.resolutions = []

    def __repr__(self):
        ruleStringList = []
        for r in self.body:
            ruleStringList.append(str(r))
        return '{head}:-{body}.'.format(head=str(self.head), body=','.join(ruleStringList))

    def unify(self, factList: [fact], contextList: [context]) -> [dict]:
        for li in self.body:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))
            li.show()

        new_fact_df = self.body[0].df
        for i in range(0, len(self.body) - 1):
            if new_fact_df.empty:
                return
            elif not self.body[i + 1].df.empty:
                common_variables = list(set(new_fact_df.columns).intersection(set(self.body[i + 1].df.columns)))
                # print(common_variables)
                new_fact_df = pd.merge(new_fact_df, self.body[i + 1].df, on=common_variables).drop_duplicates()\
                    .reset_index(drop=True)
            else:
                return
        print(new_fact_df)

        self.resolutions = []
        for _, row in new_fact_df.iterrows():
            self.resolutions.append(row.to_dict())

        return self.resolutions

    def new_facts(self, resolutions: [dict] = None) -> [fact]:
        facts = []
        if resolutions is None:
            resolutions = self.resolutions
        for resolution in resolutions:
            new_fact = self.head.generate_name_fact(resolution)
            facts.append(new_fact)
        return facts
