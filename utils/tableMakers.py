import numpy as np

# 階段や組を構成する関数群


def makeTables(cards, info):
    """
    手札と通知情報から階段と組を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser.py

    Return
    ------
    (sequence_table, pair_table)

    sequence_table: np.array((5,15))
        階段の構成を示す配列
    pair_table: np.array((5,15))
        組の構成を示す配列
    """
    if info['have_joker']:
        sequence_table = makeJSequence(cards)
        pair_table = makeJPair(cards)
    else:
        sequence_table = makeSequence(cards)
        pair_table = makePair(cards)
    return sequence_table, pair_table

# Makers     -----
# Sequence ---
# Base --


def makeBaseSequence(cards, counter):
    """
    階段を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    counter: class Counter or jCounter
        枚数のカウント方法示すクラスインスタンス

    Return
    ------
    sequence_table: np.array((5,15))
        各カードに対してそのカードを最弱として構成出来る階段の最大枚数を格納した配列
    """
    sequence_table = np.zeros_like(cards, dtype=int)
    for suit in range(4):
        for rank in reversed(range(15)):
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
    """
    JOKERを考慮し, 階段を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列

    Return
    ------
    np.array((5,15))
        各カードに対してそのカードを最弱として構成出来る階段の最大枚数を格納した配列
    """
    counter = jCounter()
    return makeBaseSequence(cards, counter)


def makeSequence(cards):
    """
    JOKERを考慮せず, 階段を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列

    Return
    ------
    np.array((5,15))
        各カードに対してそのカードを最弱として構成出来る階段の最大枚数を格納した配列
    """
    counter = Counter()
    return makeBaseSequence(cards, counter)

# counter struct --
# Joker非考慮のカウンタ


class Counter(object):
    def __init__(self):
        self.count = 0

    def update(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def get(self):
        return self.count

# Joker考慮のカウンタ


class jCounter(object):
    def __init__(self):
        self.jcount = 0
        self.count = 0

    def update(self):
        self.jcount += 1
        self.count += 1

    def reset(self):
        self.jcount = self.count + 1
        self.count = 0

    def get(self):
        return self.jcount

# Pair ---
# Base --


def makeBasePair(cards, sum_vec):
    """
    組を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    sum_vec: np.array(15)
        各ランクのカード枚数の合計

    Return
    ------
    pair_table: np.array((5,15))
        各カードに対してそのカードを含んで構成出来る組の最大枚数を格納した配列
    """
    pair_table = np.zeros_like(cards, dtype=int)
    for rank in range(15):
        if sum_vec[rank] >= 2:
            pair_table[:4, rank] = cards[:4, rank] * sum_vec[rank]
    return pair_table

# Helper --


def makeJPair(cards):
    """
    JOKERを考慮し, 組を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列

    Return
    ------
    np.array((5,15))
        各カードに対してそのカードを含んで構成出来る組の最大枚数を格納した配列
    """
    # 各カードに対してそのカードを含む組の最大枚数を格納する(Jokerも考慮する)
    sum_vec = cards[:4, :].sum(axis=0) + 1
    return makeBasePair(cards, sum_vec)


def makePair(cards):
    """
    JOKERを考慮せず, 組を構成する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列

    Return
    ------
    np.array((5,15))
        各カードに対してそのカードを含んで構成出来る組の最大枚数を格納した配列
    """
    # 各カードに対してそのカードを含む組の最大枚数を格納する(Jokerを考慮しない)
    sum_vec = cards[:4, :].sum(axis=0)
    return makeBasePair(cards, sum_vec)
