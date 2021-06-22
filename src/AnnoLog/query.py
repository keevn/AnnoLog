from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.context import context
from AnnoLog.fact import fact


class query(literal):
    def __init__(self, predicate: str, arguments: [str], ct=None):
        super(query, self).__init__(predicate, arguments, ct)

    def generate_query_result(self, resolution):
        arguments = []
        for arg in self.arguments:
            if isinstance(arg, variable):
                if str(arg) in resolution:
                    arguments.append(resolution[str(arg)])
                    print(str(arg), "=", resolution[str(arg)],".")
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
        if len(ctList) == 0:
            ctList = None
        return fact(self.predicate, arguments, ct=ctList, genetic=True)
