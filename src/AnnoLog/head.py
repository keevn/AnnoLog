from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.context import context
from AnnoLog.fact import fact


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
        ct = None
        if isinstance(self.context.name, variable):
            if str(self.context.name) in resolution:
                ct = context(resolution[str(self.context.name)])
        else:
            ct = self.context
        return fact(self.predicate, arguments, ct=ct, genetic=False)
