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

    def unify(self, l) -> dict:
        unified_Variable = {}

        if l.context is None:
            return None

        for ct in l.context:
            if isinstance(ct.name, variable):
                unified_Variable[ct.name.varName] = self.name
            elif self.name != ct.name:
                return None

        if l.predicate in self.dims:
            if len(l.arguments) != len(self.dims[l.predicate].arguments):
                return None
            for i, argument in enumerate(l.arguments):
                if isinstance(argument, variable):
                    unified_Variable[argument.varName] = self.dims[l.predicate].arguments[i]
                elif self.dims[l.predicate].arguments[i] != argument:
                    return None
        else:
            return None

        return unified_Variable
