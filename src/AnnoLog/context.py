import re

import AnnoLog.fact
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

    def unify(self, literal) -> dict:
        unified_Variable = {}

        if literal.context is None:
            return None

        for ct in literal.context:
            if isinstance(ct.name, variable):
                unified_Variable[ct.name.varName] = self.name
            elif self.name != ct.name:
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

    @staticmethod
    def parseContext(line):
        constant_name_pattern = re.compile(r'[a-z][a-z|\d|_]*')
        constant_value_pattern = re.compile(r'[a-z|\d|_]*')
        attribute_value_pattern = re.compile(r'[\s]*\'[\s]*([a-z|\d|_|\*|,|\s]*)[\s]*\'[\s]*')
        context_pattern = re.compile(
            r'[\s]*([a-z][a-z|\d|_]*)[\s]*=[\s]*{([a-z|\d|_|,|\*|\'|:|\s\[\]]*)}')

        m = context_pattern.match(line)
        if m:
            context_components = list(m.groups())
            # print(context_components)

            if constant_name_pattern.fullmatch(context_components[0].strip()):
                name = context_components[0].strip()
            else:
                return None

            literal_pattern = re.compile(
                r'([\s]*\'[\s]*[a-z|\d|_]*[\s]*\'[\s]*:[\s]*\[[\'|\d|a-z|_|,|\s|\*]*\][\s]*)')

            find_match = True
            literal_string_list = re.findall(literal_pattern, context_components[1])

            # if the concatenation of literal_string after parsing does not match the original
            # then there are some illegal literal form exist
            if context_components[1] == ','.join(literal_string_list):
                dims = {}
                for literal_string in literal_string_list:
                    literal_parts_pattern = re.compile(
                        r'[\s]*\'[\s]*([a-z|\d|_]*)[\s]*\'[\s]*:[\s]*\[([\'|\d|a-z|_|,|\*|\s]*)\]')

                    literal_string_m = literal_parts_pattern.match(literal_string)
                    # print(literal_string_m.groups())
                    literal_components = list(literal_string_m.groups())
                    predicate = literal_components[0].strip()
                    # print(literal_components[1])
                    arguments = re.findall(re.compile(r'(\'[\d|a-z|_|,|\*|\s]*\')'), literal_components[1])
                    # print(arguments)
                    for i, arg in enumerate(arguments):

                        arg = attribute_value_pattern.match(arg).groups()[0]

                        if arg is None or arg == '':
                            find_match = False
                            break

                        else:
                            arguments[i] = arg.strip()

                    dims[predicate] = AnnoLog.fact.fact(predicate, arguments)

                if find_match:
                    return context(name, dims)

            else:
                return None



        return None
