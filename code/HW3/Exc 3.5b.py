# Excercise 3.5b
def plus():
    print '+',
    for x in xrange(0,4):
        for y in xrange(0,5):
            print ' -',
        print '+',

def back():
    print '/',
    for x in xrange(0,4):
        for y in xrange(0,5):
            print '  ',
        print '/',

def display():
    for x in xrange(0,4):
        plus()
        print ''
        for y in xrange(0,3):
            back()
            print '' 
    plus()
    print ''
display() 