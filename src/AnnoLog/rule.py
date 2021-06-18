import pandas as pd


class rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body
        self.new_fact_df = None

    def __repr__(self):
        ruleStringList = []
        for r in self.body:
            ruleStringList.append(str(r))
        return '{head}:-{body}.'.format(head=str(self.head),body = ','.join(ruleStringList))

    def unify(self, factList, contextList):
        for li in self.body:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))

        self.new_fact_df = self.body[0].df
        for i in range(0, len(self.body) - 1):
            if self.new_fact_df.empty:
                self.new_fact_df = self.body[i + 1].df
            elif not self.body[i + 1].df.empty:
                self.new_fact_df = pd.merge(self.new_fact_df, self.body[i + 1].df)

    def new_facts(self):
        if self.new_fact_df is None:
            print("Please do unification first!")
            return None
        facts = []
        for index, row in self.new_fact_df.iterrows():
            new_fact = self.head.generate_name_fact(row.to_dict())
            facts.append(new_fact)
        return facts
