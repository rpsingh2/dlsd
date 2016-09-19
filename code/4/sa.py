import random
import math
import sys

"""
How to read output:

(current energy)         (Jump information)
   |                            |
   V                            V
1e-08       |......?.?..!......+...+........!......!..............

"." = trial complete
"?" = jump to worse solution
"+" = jump to better solution
"!" = jump to better solution, also happens to be best solution found thus far

As progress is made, SA will chose more appropriate solutions. IE less "?" and more "!" and "+". Once energy reaches 0, SA has determined the optimal solution.
"""

#allows print to same line
def say(x): 
    sys.stdout.write(str(x)); sys.stdout.flush()

#normalizes energy from 0-1
def energy_norm(f1, f2, min_f, max_f):
    return float((f1 + f2) - min_f) / (max_f - min_f)

def P(old, new, t):
    try:
        ans = math.exp((old-new)/t)
    # sometimes returns ans that is too large
    # if thats the case, just make ans bigger than 1
    except OverflowError:
        ans = 2
    return ans

#picks random neighbor between (x-dev) and (x+dev)
def neighbor(x, dev, min_x, max_x):
    new_x = x + random.randint((-1 * dev), dev);
    while new_x < min_x or new_x > max_x:
	new_x = x + random.randint( (-1 * dev), dev);
    return new_x

#formatting for display
def set_str_size(string, n):
    while len(string) < n:
        string = string + " "
    return string

#random.seed(1)
max_trials = 5000
t = emax =0
best_energy = energy = 1 #set to max en level
best_x = current_x = start_x = random.randint(-100000, 100000)

#print starting position of x
print "Starting x_: " + str(current_x)

#while trials still available and current energy is greater than max energy
#do SA
while t < max_trials and energy > emax:
    #find new neighbor
    new_x = neighbor(current_x, 1000, -100000, 100000)
    t += 1

    #get values of f1 and f2 given x
    f1 = new_x ** 2
    f2 = (new_x - 2) ** 2

    #determine energy
    new_energy = energy_norm(f1, f2, 2, 20000400004);
    
    rand = random.random();
    p_power = P(energy, new_energy, float(t)/max_trials)
    
    #if new energy is less than best energy,
    #NEW BEST FOUND
    #    move to new x
    #    set best energy to current energy
    if new_energy < best_energy:
        best_x = current_x = new_x
        best_energy = energy = new_energy
        say("!")

    #else if new energy is less than current energy
    #JUMP TO BETTER POINT
    #set current x to new x
    #set current energy to new energy
    elif new_energy < energy:
        current_x = new_x
        energy = new_energy
    	say("+")

    #else if P is less than random
    #(Equation for P found at bottom of page https://github.com/txt/ase16/blob/master/doc/talk3sa.md)
    #JUMP TO WORSE POINT
    elif P(energy, new_energy, float(t)/max_trials) < random.random():
	current_x = new_x
	energy = new_energy
	say("?") 
    
    #trial complete
    say(".")

    #get current energy as string
    print_en = str(round(energy,9))

    #if 50 trials completed
    #   make new line, print current energy
    if t % 50 == 0: say("\n" + set_str_size(print_en, 12) + "|")

#print out best point and best energy
print "\n\nbest results: x="+str(best_x)+" energy="+str(best_energy)
