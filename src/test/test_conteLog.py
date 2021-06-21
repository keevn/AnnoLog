import unittest
from AnnoLog.literal import literal
from AnnoLog.variable import variable
from AnnoLog.fact import fact
from AnnoLog.context import context
from AnnoLog.rule import rule
from AnnoLog.conteLog import ConteLog
from AnnoLog.head import head
from AnnoLog.body import body
from AnnoLog.builtin_predicate import unequal


class conteLogCase(unittest.TestCase):
    def test_conteLog1(self):
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

        self.assertEqual('a(parrot,bird).'
                         '\na(frog,amph).'
                         '\na(parakeet,parrot).'
                         '\na(tods,frog).'
                         '\n**a(parrot,bird)@cbird.'
                         '\n**a(frog,amph)@camph.'
                         '\n**a(parakeet,bird)@cbird.'
                         '\n**a(tods,amph)@camph.'
                         '\n**f(parrot,canfly)@cbird.'
                         '\n**f(frog,canswim)@camph.'
                         '\n**f(parakeet,canfly)@cbird.'
                         '\n**f(tods,canswim)@camph.', str(contelogCode))

    def test_conteLog2(self):
        f1 = fact('word', ['door'])
        f2 = fact('word', ['sky'])
        f3 = fact('$arabic', ['ca1'])
        f4 = fact('$arabic', ['ca2'])
        f5 = fact('$farsi', ['cf1'])
        f6 = fact('$farsi', ['cf2'])

        cf1 = context('cf1')
        cf1.add_dim(fact('meaning', ['door', 'dar']))
        cf2 = context('cf2')
        cf2.add_dim(fact('meaning', ['sky', 'asaman']))
        ca1 = context('ca1')
        ca1.add_dim(fact('meaning', ['door', 'bab']))
        ca2 = context('ca2')
        ca2.add_dim(fact('meaning', ['sky', 'samaa']))

        factList = [f1, f2, f3, f4, f5, f6]
        contextList = [cf1, cf2, ca1, ca2]

        # in order to support the '+' sign, the context argument has to be a list
        # for just one context literal like 'english_arabic(X,Y)@C'  ct=[context(variable('C'))]
        # for context in form 'C+W' literal like 'english_arabic(X,Y)@C+W'
        #       then ct=[context(variable('C')),context(variable('W'))], beware the order matters
        h = head('english_arabic', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('word', [variable('X')])
        l2 = literal('meaning', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l3 = literal('$arabic', [variable('C')])

        b = body([l1, l2, l3])

        rule1 = rule(h, b)

        h = head('english_farsi', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('word', [variable('X')])
        l2 = literal('meaning', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l3 = literal('$farsi', [variable('C')])

        b = body([l1, l2, l3])

        rule2 = rule(h, b)

        h = head('arabic_farsi', [variable('Y'), variable('Z')], ct=[context(variable('C')), context(variable('W'))])
        l1 = literal('english_arabic', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l2 = literal('english_farsi', [variable('X'), variable('Z')], ct=[context(variable('W'))])

        b = body([l1, l2])

        rule3 = rule(h, b)

        # all_translations(X, Y) @ C: -word(X), meaning(X, Y) @ C.
        h = head('all_translations', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        l1 = literal('word', [variable('X')])
        l2 = literal('meaning', [variable('X'), variable('Y')], ct=[context(variable('C'))])
        b = body([l1, l2])

        rule4 = rule(h, b)


        # across_translation(X, Y) @ C + W: -all_translations(Z, X) @ C, all_translations(Z, Y) @ W.

        h = head('across_translation', [variable('X'), variable('Y')], ct=[context(variable('C')),context(variable('W'))])
        l1 = literal('all_translations', [variable('Z'),variable('X')], ct=[context(variable('C'))])
        l2 = literal('all_translations', [variable('Z'), variable('Y')], ct=[context(variable('W'))])
        e1 = unequal([variable('C'), variable('W')])

        b = body([l1, l2], [e1])

        rule5 = rule(h, b)

        rules = [rule1, rule2, rule3, rule4, rule5]

        contelogCode = ConteLog(factList, contextList, rules)

        contelogCode.unify()

        print(str(contelogCode))

        self.assertEqual('word(door).'
                         '\nword(sky).'
                         '\n$arabic(ca1).'
                         '\n$arabic(ca2).'
                         '\n$farsi(cf1).'
                         '\n$farsi(cf2).'
                         '\n**english_arabic(door,bab)@ca1.'
                         '\n**english_arabic(sky,samaa)@ca2.'
                         '\n**english_farsi(door,dar)@cf1.'
                         '\n**english_farsi(sky,asaman)@cf2.'
                         '\n**all_translations(door,dar)@cf1.'
                         '\n**all_translations(door,bab)@ca1.'
                         '\n**all_translations(sky,asaman)@cf2.'
                         '\n**all_translations(sky,samaa)@ca2.'
                         '\n**arabic_farsi(bab,dar)@ca1+cf1.'
                         '\n**arabic_farsi(samaa,asaman)@ca2+cf2.'
                         '\n**across_translation(dar,bab)@cf1+ca1.'
                         '\n**across_translation(bab,dar)@ca1+cf1.'
                         '\n**across_translation(asaman,samaa)@cf2+ca2.'
                         '\n**across_translation(samaa,asaman)@ca2+cf2.', str(contelogCode))


if __name__ == '__main__':
    unittest.main()
