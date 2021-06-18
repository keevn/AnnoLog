from AnnoLog.variable import variable


class context:
    def __init__(self, *args):
        if len(args) == 1:
            self.name = args[0]
            self.dims = {}

        if len(args) == 2:
            self.name = args[0]
            self.dims = args[1]

    def add_dim(self, dim):
        self.dims[dim.predicate] = dim

    def __repr__(self):
        dimsList = []
        for item in self.dims.values():
            dimsList.append("'{predicate}':['{arguments}']".
                            format(predicate=item.predicate, arguments='\',\''.join(item.arguments)))

        return "{name}={{{factList}}}".format(name=self.name, factList=','.join(dimsList))

    def __eq__(self, other):
        if other is None:
            return False
        common_pairs = dict()
        for key in self.dims:
            if key in other.dims and self.dims[key] == other.dims[key]:
                common_pairs[key] = self.dims[key]

        return self.name == other.name and len(common_pairs) == len(self.dims)

    def unify(self, literal):
        unified_Variable = {}

        if literal.context is None:
            return None

        if isinstance(literal.context.name, variable):
            unified_Variable[literal.context.name.varName] = self.name
        elif self.name != literal.context.name:
            return None

        if literal.predicate in self.dims:
            if len(literal.arguments) != len(self.dims[literal.predicate].arguments):
                return None
            for i, argument in enumerate(literal.arguments):
                if isinstance(argument, variable):
                    unified_Variable[argument.varName] = self.dims[literal.predicate].arguments[i]
                elif self.dims[literal.predicate].arguments[i] != argument:
                    return None
        else:
            return None

        return unified_Variable
