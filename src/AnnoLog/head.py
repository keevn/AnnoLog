from AnnoLog.context import context
from AnnoLog.fact import fact
from AnnoLog.literal import literal
from AnnoLog.variable import variable


class head(literal):
    def __init__(self, predicate: str, arguments: [str], ct=None):
        super(head, self).__init__(predicate, arguments, ct)

    def generate_name_fact(self, resolution):
        arguments = []
        for arg in self.arguments:
            if isinstance(arg, variable):
                if str(arg) in resolution:
                    arguments.append(resolution[str(arg)])
                else:
                    break
            else:
                arguments.append(arg)
        ctList = []
        if self.context is not None:
            for ct in self.context:
                if isinstance(ct.name, variable):
                    if str(ct.name) in resolution:
                        ctList.append(context(resolution[str(ct.name)]))
                else:
                    ctList.append(ct)
        if len(ctList)==0:
            ctList = None
        return fact(self.predicate, arguments, ct=ctList, genetic=False)

    @staticmethod
    def parseHead(line):
        li = literal.parseLiteral(line)
        return head(li.predicate, li.arguments, ct=li.context)
