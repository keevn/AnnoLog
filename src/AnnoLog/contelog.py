from AnnoLog.fact import fact


class ConteLog:
    def __init__(self, factList, contextList, rules):
        self.facts = []
        self.new_facts = factList
        self.contextList = contextList
        self.rules = rules
        self.initialized = False

    def query(self, q):
        for f in self.facts:
            q.add_match(f.unify(q))

        if len(q.df.shape[0]) == 0:
            print('no.')
        else:
            print('yes.')
            for _, row in q.df.iterrows():
                print(q.generate_query_result(row.to_dict()))

    def unify(self):
        while len(self.new_facts) != 0:
            # unify each rules first
            for r in self.rules:
                r.unify(self.new_facts, self.contextList)
            self.facts.extend(self.new_facts)

            # generate new facts from unification result
            self.new_facts = []
            for r in self.rules:
                new_f = r.new_facts()
                for f in new_f:
                    if f not in self.facts and f not in self.new_facts:
                        self.new_facts.append(f)

    def all_facts(self) -> [fact]:
        return self.facts

    def __repr__(self):
        factStringList = []
        for f in self.facts:
            factStringList.append(str(f))
        return '\n'.join(factStringList)
