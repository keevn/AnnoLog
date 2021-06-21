import os
import fileinput
import re
from AnnoLog.context import context
from AnnoLog.fact import fact

cwd = os.getcwd()
sepa = os.sep
path = f'{cwd}{sepa}'
codefile_name = 'test/code1.txt' # input('code file : ')
contextfile_name = 'test/context1.txt' # input('context file : ')
codefile = path+codefile_name
contextfile = path+contextfile_name

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

x = 1
for line in fileinput.input(files=contextfile):
    print(f'{line.strip()}')
    # ct = context.parseContext(line.strip())
    constant_pattern = re.compile(r'[a-z][a-z|\d|_]*')
    context_pattern = re.compile(
        r'([a-z][a-z|\d|_]*)={([a-z|\d|_|,|\'|:|\b]*)}')

    m = context_pattern.match(line)
    # cbird = {'type': ['bird'], 'f': ['canfly']}
    if m:
        context_components = list(m.groups())
        print(context_components)
        name = context_components[0]

    #if ct is not None:
    #    contextList.append(ct)
    x += 1

print('------------------------')
for ct in contextList:
    print(ct)

