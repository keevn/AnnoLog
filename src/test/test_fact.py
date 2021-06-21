import unittest
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.literal import literal
from AnnoLog.variable import variable
import re


class factsCase(unittest.TestCase):
    def test_factConstructor(self):
        f1 = fact('word', ['door'])  # word(door)
        ct = context('j1')
        f2 = fact('p', ['4', '5'], ct=[ct])  # p(4,5)@j1
        # print(f2)
        f3 = fact('a', ['parakeet', 'parrot'], ct=[context('cbird')], genetic=False)  # a(parakeet,parrot)@cbird
        self.assertEqual(True, str(f1) == 'word(door).')
        self.assertEqual(True, str(f2) == 'p(4,5)@j1.')
        f2.setNew()
        self.assertEqual(True, '**p(4,5)@j1.' == str(f2))
        self.assertEqual(True, str(f3) == '**a(parakeet,parrot)@cbird.')
        ct.add_dim(f3)
        ct.add_dim(f1)
        ct2 = context('j1')

        ct2.add_dim(fact('word', ['door']))
        ct2.add_dim(fact('a', ['parakeet', 'parrot'], ct=[context('cbird')]))

        #print(ct)
        #print(ct2)
        self.assertEqual(True, ct == ct2 )

        f4 = fact('word', ['door'])
        #print(f4)
        self.assertEqual(True, f1 == f4)

    def test_factUnification(self):
        f1 = fact('word', ['door'])
        l1 = literal('word', [variable('X')])
        # print(f1.unify(l1))
        self.assertEqual({'X': 'door'}, f1.unify(l1))

        f2 = fact('person', ['ammar', 'canada'])
        l2 = literal('person', ['ammar', 'canada'])
        # print("f2.unify(l2): " + str(f2.unify(l2)))

        f3 = fact('person', ['ammar', 'canada'], ct=[context('j1')])
        f4 = fact('person', ['ammar', 'canada'])
        l3 = literal('person', [variable('X'), variable('Y')], ct=[context('j1')])
        l4 = literal('person', [variable('X'), variable('Y')], ct=[context(variable('Z'))])
        #print(f3.unify(l3))
        #print(f4.unify(literal('person', [variable('X'), 'france'])))
        self.assertEqual(None,f4.unify(literal('person', [variable('X'), 'france'])))
        self.assertEqual({'Y': 'canada', 'X': 'ammar'}, f3.unify(l3))
        self.assertEqual({'X': 'ammar', 'Z': 'j1', 'Y': 'canada'}, f3.unify(l4))

    def test_parseFact(self):
        text = 'a(parrot,bird,birda).'
        f = fact.parseFact(text)
        self.assertEqual(text, str(f))

        text = 'a(parrot,bird,birda)@a.'
        f = fact.parseFact(text)
        self.assertEqual(text, str(f))

        text = 'a(parrot,bird,birda)@a+.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'A(parrot,bird,birda)@a.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'aA(parrot,bird,birda)@a.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'aa (parrot,bird,birda)@a.'
        f = fact.parseFact(text)
        self.assertEqual('aa(parrot,bird,birda)@a.', str(f))

        text = 'a ab(parrot,bird,birda)@a.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'abc   (  parrot  ,  bird, birda   ) @  a + b .'
        f = fact.parseFact(text)
        self.assertEqual('abc(parrot,bird,birda)@a+b.', str(f))

        text = 'a   (  parrot  ,  bird, bir da   )@  a + b .'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'abc   (  parrot  ,  bird, birda   )@  aa + b b.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'a(parrot,bird,birda)@A.'
        f = fact.parseFact(text)
        self.assertEqual(None, f)

        text = 'a(parrot,bird,,birda)@a+b  .'
        f = fact.parseFact(text)
        self.assertEqual(None, f)


if __name__ == '__main__':
    unittest.main()
