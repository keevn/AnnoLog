from AnnoLog.variable import variable


class fact:
    def __init__(self, predicate: str, arguments: [str], ct=None, genetic: bool = True):
        self.genetic = genetic
        self.predicate = predicate
        self.arguments = arguments
        self.context = ct

    def __repr__(self):
        return '{sign}{predicate}({arguments}){context}'. \
            format(sign='' if self.genetic else '**',
                   predicate=self.predicate,
                   arguments=','.join(self.arguments),
                   context='' if self.context is None else '@' + str(self.context.name))

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
                if isinstance(literal.context.name, variable):
                    unified_Variable[literal.context.name.varName] = self.context.name
                elif self.context != literal.context:
                    return None

            # after checking the context, check all the arguments
            for i, argument in enumerate(literal.arguments):
                if isinstance(argument, variable):
                    unified_Variable[argument.varName] = self.arguments[i]
                elif self.arguments[i] != argument:
                    return None

        return unified_Variable


