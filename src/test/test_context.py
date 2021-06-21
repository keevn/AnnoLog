import unittest
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.literal import literal
from AnnoLog.variable import variable


class contextCase(unittest.TestCase):
    def test_contextUnification(self):
        ct = context('c1')
        ct.add_dim(fact('currency', ['euro']))
        ct.add_dim(fact('location', ['france']))
        print(ct)
        l1 = literal('location', [variable('Y')], ct=[context(variable('C'))])
        l2 = literal('location', [variable('Y')], ct=[context('c1')])
        print(l1)
        print(l2)
        self.assertEqual({'C': 'c1', 'Y': 'france'}, ct.unify(l1))
        self.assertEqual({'Y': 'france'}, ct.unify(l2))

        l3 = literal('currency', [variable('Z')], ct=[context(variable('C'))])
        print(l3)
        print(ct.unify(l3))

        cf1 = context('cf1')
        cf1.add_dim(fact('meaning', ['door']))
        l4 = literal('meaning', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        print(cf1)
        print(l4)
        self.assertEqual(None, cf1.unify(l4))

        cf1.add_dim(fact('meaning', ['door', 'dar']))
        print(cf1.unify(l4))
        self.assertEqual({'C': 'cf1', 'X': 'door', 'Y': 'dar'}, cf1.unify(l4))

        l5 = literal('meaning', ['door', variable('Y')], ct=[context(variable('C'))])
        print(cf1.unify(l5))


if __name__ == '__main__':
    unittest.main()
