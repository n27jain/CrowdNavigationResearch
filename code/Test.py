

ar = []

from MapObjects import *

from random import choice

a = [1,2,3,4,5,6]
b = [1,4]

for j in range(100):
    c = choice([i for i in range(1,len(a)) if i not in b])
    print(c)
