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
import os
import fileinput


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

        print(str(contelogCode))

        query_literal = query('a', [variable('X'), variable('Z')])
        print("Query string :", str(query_literal))

        count = contelogCode.query(query_literal)
        self.assertEqual(4, count)

        query_literal = query('ab', [variable('X'), variable('Z')])
        print("\nQuery string :", str(query_literal))

        count = contelogCode.query(query_literal)

        self.assertEqual(0, count)

        query_literal = query('f', ['frog', variable('Z')],[context(variable('C'))])
        print("\nQuery string :", str(query_literal))

        count = contelogCode.query(query_literal)

        self.assertEqual(1, count)

    def test_query2(self):
        cwd = os.getcwd()
        sepa = os.sep
        path = f'{cwd}{sepa}'
        codefile_name = 'code3.txt'  # input('code file : ')
        contextfile_name = 'context3.txt'  # input('context file : ')
        codefile = path + codefile_name
        contextfile = path + contextfile_name

        factList = []
        contextList = []
        rules = []
        for line in fileinput.input(files=codefile):
            f = fact.parseFact(line.strip())
            if f is not None:
                factList.append(f)

            r = rule.parseRule(line.strip())
            if r is not None:
                rules.append(r)

        for line in fileinput.input(files=contextfile):
            ct = context.parseContext(line.strip())

            if ct is not None:
                contextList.append(ct)

        contelogCode = ConteLog(factList, contextList, rules)

        contelogCode.unify()

        print(str(contelogCode))

        query_literal = query('p', ['2', variable('Q')])
        print("Query string :", str(query_literal))

        count = contelogCode.query(query_literal)
        self.assertEqual(3, count)


if __name__ == '__main__':
    unittest.main()
