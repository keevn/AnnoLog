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
        self.resolutions = self.body.unify(factList, contextList)
        return self.resolutions

    def new_facts(self, resolutions: [dict] = None) -> [fact]:
        facts = []
        if resolutions is None:
            resolutions = self.resolutions

        # check whether resolution is None again because self.resolutions might be None as well
        if resolutions is not None:
            for resolution in resolutions:
                new_fact = self.head.generate_name_fact(resolution)
                facts.append(new_fact)
        return facts

    @staticmethod
    def parseRule(line):
        return None
