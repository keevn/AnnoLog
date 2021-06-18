import unittest
from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.rule import rule
from AnnoLog.ConteLog import ConteLog


class conteLogCase(unittest.TestCase):
    def test_conteLog(self):
        f1 = fact('a', ['parrot', 'bird'])
        f2 = fact('a', ['frog', 'amph'])
        f3 = fact('a', ['parakeet', 'parrot'])
        f4 = fact('a', ['tods', 'frog'])

        c1 = context('cbird')
        c1.add_dim(fact('type', ['bird']))
        c1.add_dim(fact('f', ['canfly']))
        c2 = context('camph')
        c2.add_dim(fact('type', ['amph']))
        c2.add_dim(fact('f', ['canswim']))

        factList = [f1, f2, f3, f4]
        contextList = [c1, c2]

        head = literal('a', [variable('X'), variable('Y')], ct=context(variable('C')))
        l1 = literal('a', [variable('X'), variable('Y')])
        l2 = literal('type', [variable('Y')], ct=context(variable('C')))

        body = [l1, l2]

        rule1 = rule(head, body)

        head = literal('a', [variable('X'), variable('Y')], ct=context(variable('C')))
        l1 = literal('a', [variable('X'), variable('Z')])
        l2 = literal('a', [variable('Z'), variable('Y')], ct=context(variable('C')))

        body = [l1, l2]

        rule2 = rule(head, body)

        head = literal('f', [variable('X'), variable('Y')], ct=context(variable('C')))
        l1 = literal('a', [variable('X'), variable('Z')], ct=context(variable('C')))
        l2 = literal('f', [variable('Y')], ct=context(variable('C')))

        body = [l1, l2]

        rule3 = rule(head, body)

        rules = [rule1, rule2, rule3]

        contelogCode = ConteLog(factList, contextList, rules)

        contelogCode.unify()

        print(str(contelogCode))


if __name__ == '__main__':
    unittest.main()
