class variable:

    def __init__(self, name):
        self.varName = name.capitalize()

    def __eq__(self, other):
        if not isinstance(other, variable):
            return False
        return self.varName == other.varName

    def __repr__(self):
        return self.varName
