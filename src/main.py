import os
import fileinput
import re
from AnnoLog.context import context
from AnnoLog.fact import fact

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
x = 1
for line in fileinput.input(files=codefile):
    print(f'{line.strip()}')
    f = fact.parseFact(line.strip())
    if f is not None:
        factList.append(f)
    x += 1

print('------------------------')
for f in factList:
    print(f)

print()
x = 1
for line in fileinput.input(files=contextfile):
    print(f'{line.strip()}')
    ct = context.parseContext(line.strip())

    if ct is not None:
        contextList.append(ct)
    x += 1

print('------------------------')
for ct in contextList:
    print(ct)
