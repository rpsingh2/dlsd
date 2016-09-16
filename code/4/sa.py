import random
import math
import sys

def say(x): 
    sys.stdout.write(str(x)); sys.stdout.flush()

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

def neighbor(x, dev, min_x, max_x):
    new_x = x + random.randint((-1 * dev), dev);
    while new_x < min_x or new_x > max_x:
	new_x = x + random.randint( (-1 * dev), dev);
    return new_x

def set_str_size(string, n):
    while len(string) < n:
        string = string + " "
    return string

#random.seed(1)
max_trials = 5000
t = emax =0
best_energy = energy = 1 #set to max en level
best_x = current_x = start_x = random.randint(-100000, 100000)

print "Starting x_: " + str(current_x)

while t < max_trials and energy > emax:
    new_x = neighbor(current_x, 1000, -100000, 100000)
    t += 1
    f1 = new_x ** 2
    f2 = (new_x - 2) ** 2

    new_energy = energy_norm(f1, f2, 2, 20000400004);
    
    rand = random.random();
    p_power = P(energy, new_energy, float(t)/max_trials)
    if new_energy < best_energy:
        best_x = current_x = new_x
        best_energy = energy = new_energy
        say("!")
    elif new_energy < energy:
        current_x = new_x
        energy = new_energy
    	say("+")
    elif P(energy, new_energy, float(t)/max_trials) < random.random():
	current_x = new_x
	energy = new_energy
	say("?") 
    say(".")
    #print current_x
    print_en = str(round(energy,9))
    if t % 50 == 0: say("\n" + set_str_size(print_en, 12) + "|")

print "\n\nbest results: x="+str(best_x)+" energy="+str(best_energy)
