# Excercise 3.5(a)

def plus():
    print '+',
    for x in xrange(0,2):
        for y in xrange(0,3):
            print ' -',
        print '+',

def back():
    print '/',
    for x in xrange(0,2):
        for y in xrange(0,3):
            print '  ',
        print '/',

def display():
    for x in xrange(0,2):
        plus()
        print ''
        for y in xrange(0,3):
            back()
            print '' 
    plus()
    print ''
display() 

