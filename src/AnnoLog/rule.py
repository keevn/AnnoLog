import re

from AnnoLog.body import body
from AnnoLog.context import context
from AnnoLog.fact import fact
from AnnoLog.head import head


class rule:
    def __init__(self, h: head, body):
        self.head = h
        self.body = body
        self.resolutions = []

    def __repr__(self):
        ruleStringList = []
        return '{head}:-{body}.'.format(head=str(self.head), body=str(self.body))

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
                new_fact = self.head.generate_new_fact(resolution)
                facts.append(new_fact)
        return facts

    @staticmethod
    def parseRule(line):
        rule_pattern = re.compile(
            r'[\s]*([a-z][a-z|\d|_]*[\s]*\([\s]*[a-z|A-Z][a-z|A-Z|\d|_|,|\s]*[\s]*\)[\s]*(?:@[\s]*[a-z|A-Z][a-z|A-Z|\d|_|+|\s]*)?)'
            r'[\s]*:-[\s]*([a-z|A-Z|\d|_|$|+|*|&|@|=|!|\(|\)|,|\s]*)[\s]*\.')
        m = rule_pattern.match(line)
        if m is not None:
            rule_components = list(m.groups())
            head_string = rule_components[0]
            h = head.parseHead(head_string)
            if h is not None:
                # print(h)
                body_string = rule_components[1]
                b = body.parseBody(body_string)
                if b is not None:
                    # print(b)
                    return rule(h, b)
        return None
