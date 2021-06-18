class ConteLog:
    def __init__(self, factList, contextList, rules):
        self.facts = []
        self.new_facts = factList
        self.contextList = contextList
        self.rules = rules

    def unify(self):
        while len(self.new_facts) != 0:
            for r in self.rules:
                r.unify(self.new_facts, self.contextList)
            self.facts.append(self.new_facts)
            self.new_facts = []
            for r in self.rules:
                self.new_facts.append(r.new_facts())

    def __repr__(self):
        factStringList = []
        for f in self.facts:
            factStringList.append(str(f))
        return '\n'.join(factStringList)
