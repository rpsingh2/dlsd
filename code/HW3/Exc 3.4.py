def do_twice(f,s):    
	f(s)    
	f(s)
def do_four(f,s):    
	do_twice(f,s)    
	do_twice(f,s)    

def print_twice(x):    	
	print x
do_four(print_twice,'spam')
