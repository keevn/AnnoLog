from AnnoLog.variable import variable
import AnnoLog.context
import re


class fact:
    def __init__(self, predicate: str, arguments: [str], ct: [] = None, genetic: bool = True):
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

    @staticmethod
    def parseFact(line):
        # Constants start with lowercase letter, follows with any number of lowercase letter, digits or '_'
        constant_pattern = re.compile(r'[a-z][a-z|\d|_]*')
        # Variables start with capital letter, follows with any number of capital letter, digits or '_'
        variable_pattern = re.compile(r'[A-Z][A-Z|\d|_]*')
        # facts line has three parts:
        #   predicate, arguments and contexts
        #   predicate pattern : ([\s]*[a-z][a-z|\d|_]*[\s]*)
        #   arguments pattern : \([\s]*([a-z][a-z|\d|_|,|\s]*)[\s]*\)
        #   contexts pattern : (@[\s]*[a-z][a-z|\d|_|+|\s]*)?[\s]*
        # then end with '\.'
        # [\s]* means any number of space or blank characters
        fact_pattern = re.compile(
            r'([\s]*[a-z][a-z|\d|_]*[\s]*)\([\s]*([a-z][a-z|\d|_|,|\s]*)[\s]*\)[\s]*(@[\s]*[a-z][a-z|\d|_|+|\s]*)?[\s]*\.')
        m = fact_pattern.match(line)
        if m:
            fact_components = list(m.groups())
            if constant_pattern.fullmatch(fact_components[0].strip()):
                predicate = fact_components[0].strip()
            else:
                return None
            arguments = fact_components[1].split(',')
            find_match = True
            for i, arg in enumerate(arguments):
                if arg is None or arg == '':
                    find_match = False
                    break

                # this check makes sure there is no space inside of argument name
                elif re.compile(r'([a-z|\d|_]*)').fullmatch(arg.strip()):
                    arguments[i] = arg.strip()
                else:
                    find_match = False
                    break

            ct = fact_components[-1]
            ct_list = None
            if find_match:
                if ct is not None:
                    ct_list = []
                    ct_name_list = fact_components[-1][1:].strip().split('+')
                    for ct_name in ct_name_list:
                        if ct_name is None or ct_name == '':
                            find_match = False
                            return None
                        elif constant_pattern.fullmatch(ct_name.strip()):
                            ct_list.append(AnnoLog.context.context(ct_name.strip()))
                        else:
                            find_match = False
                            break
                if find_match:
                    return fact(predicate, arguments, ct_list)

            return None

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
                # the numbers of both contexts have to match
                if len(self.context) != len(literal.context):
                    return None
                for i, ct in enumerate(literal.context):
                    if isinstance(ct.name, variable):
                        unified_Variable[str(ct.name)] = self.context[i].name
                    elif self.context[i] != ct:
                        return None

            # after checking the context, check all the arguments
            for i, argument in enumerate(literal.arguments):
                if isinstance(argument, variable):
                    unified_Variable[str(argument)] = self.arguments[i]
                elif self.arguments[i] != argument:
                    return None

        return unified_Variable


