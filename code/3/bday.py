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

count = 0
trials = 100

for x in range(trials):
    bdays = [None] * 23
    # put random bdays in list
    for x in xrange(len(bdays)):
    	bdays[x] = random.randint(1,365)
    if has_duplicates(bdays): count += 1

print "Prob bday 23 ppl: " + str(float(count)/trials)
