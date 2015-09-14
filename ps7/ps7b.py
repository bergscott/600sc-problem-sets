## 1-1. Probability 1/2 * 1/2 * 1/2 = 1/8
## 1-2. Probability 1/2 * 1/2 * 1/2 = 1/8
## 1-3. Probability P(H,H,T) + P(H,T,H) + P(T,H,H) = 1/8 + 1/8 + 1/8 = 3/8
## 1-4. P(H,H,T) + P(H,T,H) + P(T,H,H) + P(H,H,H) = 4/8 = 1/2
## 2. (1/6)**4 first roll can be any then other 4 rolls P(1/6) chance to match

import random

def roll_die():
    '''
    simulates a roll of a six-side die

    returns int in [1-6]
    '''
    return random.choice([1, 2, 3, 4, 5, 6])

def roll_yahtzee():
    '''
    simulates the roll of five dice. returns True if all five dice come up with
    the same value, otherwise returns False

    returns: boolean
    '''
    firstRoll = roll_die()
    for r in range(4):
        if roll_die() != firstRoll:
            return False
        else:
            continue
    return True

def run_trials(n):
    '''
    runs N attempts at rolling a Yahtzee! and prints summary of results.

    returns: float [0-1]
    '''
    yahtzeeCount = 0
    for t in xrange(n):
        if roll_yahtzee():
            yahtzeeCount += 1
    print "Got %i yahtzee!'s in %i attempts" % (yahtzeeCount, n)
    prob = yahtzeeCount / float(n)
    print str(prob) + ' probability of getting a yahtzee! on the' +\
          ' first roll.'
    return prob

##cumulativeProbs = 0
##for t in range(100):
##    cumulativeProbs += run_trials(10**5)
##avgProb = cumulativeProbs / float(100)
##print 'Average Probability from ' + str(100 * 10**5) + ' trials: %f' % avgProb

        
