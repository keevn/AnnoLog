import os
import fileinput

from AnnoLog.contelog import ConteLog
from AnnoLog.context import context
from AnnoLog.fact import fact
from AnnoLog.rule import rule

cwd = os.getcwd()
sepa = os.sep
path = f'{cwd}{sepa}'
codefile_name = 'test/code1.txt'  # input('code file : ')
contextfile_name = 'test/context1.txt'  # input('context file : ')
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

print('facts and rules :')
print('------------------------')
for f in factList:
    print(f)

for r in rules:
    print(r)

print()
for line in fileinput.input(files=contextfile):
    ct = context.parseContext(line.strip())

    if ct is not None:
        contextList.append(ct)

print('contexts : ')
print('------------------------')
for ct in contextList:
    print(ct)

print()
print('unification result: ')
print('------------------------')

contelogCode = ConteLog(factList, contextList, rules)

contelogCode.unify()

print(str(contelogCode))
