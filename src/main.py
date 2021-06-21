import os
import fileinput
import re
from AnnoLog.context import context
from AnnoLog.fact import fact

cwd = os.getcwd()
sepa = os.sep
path = f'{cwd}{sepa}'
codefile_name = input('code file : ')
name = path+codefile_name

factList = []
contextList = []
rules = []
x = 1
for line in fileinput.input(files=name):
    print(f'{line.strip()}')
    f = fact.parseFact(line.strip())
    if f is not None:
        factList.append(f)
    x += 1

for f in factList:
    print(f)


