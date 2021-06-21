import unittest
from AnnoLog.literal import literal
from AnnoLog.head import head
from AnnoLog.variable import variable
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.rule import rule
import pandas as pd


class ruleCase(unittest.TestCase):
    def test_rule1(self):
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
        body = [l1, l2]

        rule1 = rule(h, body)

        new_facts = rule1.new_facts(rule1.unify(factList, contextList))
        self.assertEqual(2, len(new_facts))

    def test_rule2(self):
        f1 = fact('word', ['door'])
        f2 = fact('word', ['sky'])
        f3 = fact('$arabic', ['ca1'])
        f4 = fact('$arabic', ['ca2'])
        f5 = fact('$farsi', ['cf1'])
        f6 = fact('$farsi', ['cf2'])

        # word(door).
        # word(sky).
        # $arabic(ca1).
        # $arabic(ca2).
        # $farsi(cf1).
        # $farsi(cf2).

        c1 = context('cf1')
        c1.add_dim(fact('meaning', ['door', 'dar']))
        c2 = context('cf2')
        c2.add_dim(fact('meaning', ['sky', 'asaman']))
        c3 = context('ca1')
        c3.add_dim(fact('meaning', ['door', 'bab']))
        c4 = context('ca2')
        c4.add_dim(fact('meaning', ['sky', 'samaa']))

        # cf1 = {'meaning': ['door', 'dar']}
        # cf2 = {'meaning': ['sky', 'asaman']}
        # ca1 = {'meaning': ['door', 'bab']}
        # ca2 = {'meaning': ['sky', 'samaa']}

        factList = [f1, f2, f3, f4, f5, f6]
        contextList = [c1, c2, c3, c4]

        # english_arabic(X, Y) @ C: -word(X), meaning(X, Y) @ C,$arabic(C).

        h = head('english_arabic', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('word', [variable('X')])
        l2 = literal('meaning', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l3 = literal('$arabic', [variable('C')])
        body = [l1, l2, l3]

        rule1 = rule(h, body)

        new_facts = rule1.new_facts(rule1.unify(factList, contextList))
        self.assertEqual(2, len(new_facts))
        for f in new_facts:
            print(f)

        h = head('english_farsi', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1.reset_df()
        l2.reset_df()
        l4 = literal('$farsi', [variable('C')])
        body = [l1, l2, l4]
        rule2 = rule(h, body)
        new_facts = rule2.new_facts(rule2.unify(factList, contextList))
        for f in new_facts:
            print(f)
        self.assertEqual(2, len(new_facts))


if __name__ == '__main__':
    unittest.main()
