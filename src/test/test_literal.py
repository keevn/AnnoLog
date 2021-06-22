import unittest
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.head import head
import pandas as pd


class literalCase(unittest.TestCase):
    def test_case1(self):
        f1 = fact('person', ['ammar', 'canada'])
        f2 = fact('person', ['zaki', 'france'])
        c1 = context('c1')
        c1.add_dim(fact('currency', ['euro']))
        c1.add_dim(fact('location', ['france']))
        c2 = context('c2')
        c2.add_dim(fact('currency', ['dollar']))
        c2.add_dim(fact('location', ['usa']))
        c3 = context('c3')
        c3.add_dim(fact('currency', ['cad']))
        c3.add_dim(fact('location', ['canada']))

        l1 = literal('person', [variable('X'), variable('Y')])
        l2 = literal('location', [variable('Y')], ct=[context(variable('C'))])
        l3 = literal('currency', [variable('Z')], ct=[context(variable('C'))])

        factList = [f1, f2]
        contextList = [c1, c2, c3]
        literalList = [l1, l2, l3]

        for li in literalList:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))

        df = literalList[0].df
        for i in range(0, len(literalList)-1):
            df = pd.merge(df, literalList[i+1].df)

        print(df)

        self.assertEqual(2, df.shape[0])

    def test_case2(self):
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

        l1 = literal('a', [variable('X'), variable('Y')])
        l2 = literal('type', [variable('Y')], ct=[context(variable('C'))])

        factList = [f1, f2, f3, f4]
        contextList = [c1, c2]
        literalList = [l1, l2]

        for li in literalList:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))

        df = literalList[0].df
        for i in range(0, len(literalList)-1):
            df = pd.merge(df, literalList[i+1].df)

        print(df)
        self.assertEqual(2, df.shape[0])

        head_literal = head('a', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        print(head_literal)
        for index, row in df.iterrows():
            new_fact = head_literal.generate_new_fact(row.to_dict())
            print(new_fact)
            factList.append(new_fact)

        l3 = literal('a', [variable('X'), variable('Z')])
        l4 = literal('a', [variable('Z'), variable('Y')], ct=[context(variable('C'))])
        literalList = [l3, l4]

        for li in literalList:
            for f in factList:
                li.add_match(f.unify(li))
            for c in contextList:
                li.add_match(c.unify(li))

        df = literalList[0].df
        for i in range(0, len(literalList) - 1):
            df = pd.merge(df, literalList[i + 1].df)

        print(df)
        head_literal = head('a', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        print(head_literal)
        for index, row in df.iterrows():
            new_fact = head_literal.generate_new_fact(row.to_dict())
            print(new_fact)
            factList.append(new_fact)


if __name__ == '__main__':
    unittest.main()
