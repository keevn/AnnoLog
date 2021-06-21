from AnnoLog.variable import variable
from AnnoLog.context import context


class fact:
    def __init__(self, predicate: str, arguments: [str], ct: [context] = None, genetic: bool = True):
        self.genetic = genetic
        self.predicate = predicate
        self.arguments = arguments
        self.context = ct

    def __repr__(self):
        context_str = []
        if self.context is not None:
            for ct in self.context:
                context_str.append(ct.name)

        return '{sign}{predicate}({arguments}){context}.'. \
            format(sign='' if self.genetic else '**',
                   predicate=self.predicate,
                   arguments=','.join(self.arguments),
                   context='' if self.context is None else '@' + '+'.join(context_str))

    def setNew(self):
        self.genetic = False

    def __eq__(self, other):
        if other is None:
            return False
        if self.context is None:
            if other.context is None:
                return self.predicate == other.predicate and self.arguments == other.arguments
            else:
                return False
        elif self.context != other.context:
            return False
        else:
            return self.predicate == other.predicate and self.arguments == other.arguments

    def unify(self, literal) -> dict:
        unified_Variable = {}

        # if the signature does not match then the literal can not be unified to this fact
        if self.predicate != literal.predicate or len(self.arguments) != len(literal.arguments):
            return None
        else:
            # if only one context is None then the literal can not be unified to this fact
            if self.context is None and literal.context is not None:
                return None
            if self.context is not None and literal.context is None:
                return None

            # if both contexts are not None then check the context first
            if self.context is not None and literal.context is not None:
                if len(self.context) != len(literal.context):
                    return None
                for i, ct in enumerate(literal.context):
                    if isinstance(ct.name, variable):
                        unified_Variable[ct.name.varName] = self.context[i].name
                    elif self.context[i] != ct:
                        return None

            # after checking the context, check all the arguments
            for i, argument in enumerate(literal.arguments):
                if isinstance(argument, variable):
                    unified_Variable[argument.varName] = self.arguments[i]
                elif self.arguments[i] != argument:
                    return None

        return unified_Variable


