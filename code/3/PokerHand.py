"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

from Card import *
from collections import Counter

class PokerHand(Hand):

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.

        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1
    def rank_hist(self):
	self.rank = {}
	for card in self.cards:
	    self.rank[card.rank] = self.rank.get(card.rank, 0) + 1

    def x_of_a_kind_check(self, x, y):
	self.rank_hist()
        col = Counter(self.rank.values())
        if col[x] == y:
            return True
        return False

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_pair(self):
	return self.x_of_a_kind_check(2, 1)	

    def has_twopair(self):
	return self.x_of_a_kind_check(2, 2)

    def has_three_of_a_kind(self):
        return self.x_of_a_kind_check(3, 1)
    
    def has_four_of_a_kind(self):
    	return self.x_of_a_kind_check(4, 1)
    
    def has_full_house(self):
	return self.x_of_a_kind_check(3, 1) and self.x_of_a_kind_check(2, 1)

    def has_straight(self):
    	ranks = self.rank
	count = 0
	for i in xrange(1, 15):
	    if ranks.get(i):
		count += 1
		if count == 5:
		    return True
	    else:
		count = 0
	return False

    def has_straight_flush(self):
	pair = set()
	for card in self.cards:
	    pair.add((card.rank, card.suit))
	    if card.rank == 1:
		pair.add((14, card.suit))
	
	for suit in xrange(4):
	    count = 0;
	    for rank in xrange(1, 15):
		if (rank, suit) in pair:
	            count += 1
		    if count == 5:
			return True
		else: count = 0;
	return False

if __name__ == '__main__':
    # make a deck
    deck = Deck()
    deck.shuffle()

    s_flush = straight = full_house = four_of_a_kind = three_of_a_kind = two_pair = pair = flush = 0;
    hands = [0,0,0,0,0,0,0,0]
    
    def classify(hand, hands):
        if(hand.has_straight_flush()):
                hands[0] += 1
        elif(hand.has_four_of_a_kind()):
                hands[1] += 1
        elif(hand.has_full_house()):
                hands[2] += 1
        elif(hand.has_flush()):
                hands[3] += 1
        elif(hand.has_straight()):
                hands[4] += 1
        elif(hand.has_three_of_a_kind()):
                hands[5] += 1
        elif(hand.has_twopair()):
                hands[6] += 1
        elif(hand.has_pair()):
                hands[7] += 1

    trials = 10000

    # deal the cards and classify the hands
    for i in range(trials):
        hand = PokerHand()
	deck = Deck()
	deck.shuffle()
        deck.move_cards(hand, 7)
        hand.sort()
	classify(hand, hands)
    print "Pair: " + str(float(hands[7])/trials)
    print "Two pair " + str(float(hands[6])/trials)
    print "Three of a kind " + str(float(hands[5])/trials)
    print "Straight " + str(float(hands[4])/trials)
    print "Flush " + str(float(hands[3])/trials)
    print "Full house " + str(float(hands[2])/trials)
    print "four of a kind " + str(float(hands[1])/trials)
    print "Straight flush " + str(float(hands[0])/trials)



