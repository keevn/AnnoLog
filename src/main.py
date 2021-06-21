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

fact_pattern = re.compile(r'([a-z][a-z|\d|_]*)\(([a-z][a-z|\d|_]*)([,[a-z][a-z|\d|_]*]*)\)([@[a-z][a-z|\d|_]*]?)?\.')
rule_pattern = re.compile(r'([a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?):-([a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?)(,[a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?)?\.')

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

t = 'aasdf_adsf(asdf304Adsf,dfd)@C+W:-aasdfadsf(asdfdsf,Y)@A,adfs(ASD,DE),fffdg(asdf,DDf)@C.'
rule_pattern = re.compile(r'([a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?):-([a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?)(,[a-z][a-z|\d|_]*\([a-z|\d|A-Z|_|,]*\)(?:[@[a-z|A-Z][a-z|\d|+|_|A-Z]*]?)?)*\.')

m = rule_pattern.match(t)
if m:
    print(m.groups())

