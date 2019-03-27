import numpy as np

# Makers     -----
# 全て基礎となるBase関数とそれを呼び出すだけのHelper関数から成っています


def makeTables(cards, info):
    if info['have_joker']:
        sequence_table = makeJSequence(cards)
        pair_table     = makeJPair(cards)
    else:
        sequence_table = makeSequence(cards)
        pair_table     = makePair(cards)
    return sequence_table, pair_table

# Sequence ---
# Base --
def makeBaseSequence(cards, counter, scope):
    sequence_table = np.zeros_like(cards, dtype = int)
    for suit in range(4):
        for rank in scope:
            if cards[suit, rank] == 1:
                counter.update()
            else:
                counter.reset()

            count = counter.get()
            if count >= 3:
                sequence_table[suit, rank] = count
    return sequence_table

# Helper --
def makeJSequence(cards):
    # 各カードに対してそのカードを最弱とする階段の最大枚数を格納する(Jokerも考慮する)
    counter = jCounter()
    return makeBaseSequence(cards, counter, reversed(range(15)))

def makeSequence(cards):
    # 各カードに対してそのカードを最弱とする階段の最大枚数を格納する(Jokerは考慮しない)
    counter = Counter()
    return makeBaseSequence(cards, counter, reversed(range(15)))

# Pair ---
# Base --
def makeBasePair(cards, sum_vec, scope):
    pair_table = np.zeros_like(cards, dtype = int)
    for rank in scope:
        if sum_vec[rank] >= 2:
            pair_table[:4, rank] = cards[:4, rank] * sum_vec[rank]
    return pair_table

# Helper --
def makeJPair(cards):
    # 各カードに対してそのカードを含む組の最大枚数を格納する(Jokerも考慮する)
    sum_vec  = cards[:4, :].sum(axis = 0) + 1
    return makeBasePair(cards, sum_vec, range(15))

def makePair(cards):
    # 各カードに対してそのカードを含む組の最大枚数を格納する(Jokerを考慮しない)
    sum_vec  = cards[:4, :].sum(axis = 0)
    return makeBasePair(cards, sum_vec, range(15))

# counter struct ---
class Counter(object):
    def __init__(self):
        self.count = 0
    def update(self):
        self.count += 1
    def reset(self):
        self.count = 0    
    def get(self):
        return self.count

class jCounter(object):
    def __init__(self):
        self.jcount = 0
        self.count  = 0
    def update(self):
        self.jcount += 1
        self.count  += 1
    def reset(self):
        self.jcount = self.count + 1
        self.count  = 0    
    def get(self):
        return self.jcount
