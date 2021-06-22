import unittest
from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.query import query
from AnnoLog.contelog import ConteLog
from AnnoLog.head import head
from AnnoLog.body import body
from AnnoLog.rule import rule


class queryCase(unittest.TestCase):
    def test_query1(self):
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

        h = head('a', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('a', [variable('X'), variable('Y')])
        l2 = literal('type', [variable('Y')], ct=[context(variable('C'))])

        b = body([l1, l2])

        rule1 = rule(h, b)

        h = head('a', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('a', [variable('X'), variable('Z')])
        l2 = literal('a', [variable('Z'), variable('Y')], ct=[context(variable('C'))])

        b = body([l1, l2])

        rule2 = rule(h, b)

        h = head('f', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('a', [variable('X'), variable('Z')], ct=[context(variable('C'))])
        l2 = literal('f', [variable('Y')], ct=[context(variable('C'))])

        b = body([l1, l2])

        rule3 = rule(h, b)

        rules = [rule1, rule2, rule3]

        contelogCode = ConteLog(factList, contextList, rules)

        contelogCode.unify()

        query_literal = query('a', [variable('X'), variable('Z')])
        print("Query string :", str(query_literal))

        count = contelogCode.query(query_literal)
        self.assertEqual(4, count)

        query_literal = query('ab', [variable('X'), variable('Z')])
        print("\nQuery string :", str(query_literal))

        count = contelogCode.query(query_literal)

        self.assertEqual(0, count)

if __name__ == '__main__':
    unittest.main()
