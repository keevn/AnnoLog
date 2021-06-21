class ConteLog:
    def __init__(self, factList, contextList, rules):
        self.facts = []
        self.new_facts = factList
        self.contextList = contextList
        self.rules = rules

    def query(self, line):
        pass

    def unify(self):
        while len(self.new_facts) != 0:
            for r in self.rules:
                r.unify(self.new_facts, self.contextList)
            self.facts.extend(self.new_facts)
            self.new_facts = []
            for r in self.rules:
                new_f = r.new_facts()
                for f in new_f:
                    if f not in self.facts and f not in self.new_facts:
                        self.new_facts.append(f)

    def __repr__(self):
        factStringList = []
        for f in self.facts:
            factStringList.append(str(f))
        return '\n'.join(factStringList)
