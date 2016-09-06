import random

def has_duplicates(stuff):
    for x in stuff:
	count = 0
        for y in stuff:
	    if x == y:
                count += 1
            if count > 1:
                return True
    return False

random.seed(1)
bdays = [None] * 23
for x in xrange(len(bdays)):
    bdays[x] = random.randint(1,365)

print bdays
print has_duplicates(bdays)
