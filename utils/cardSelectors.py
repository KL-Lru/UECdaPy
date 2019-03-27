import numpy as np

# 提出手を一つ載せたテーブルを返す関数群

# Sequence ---
# Base --


def selectBaseSequence(cards, sequence_table, scope):
    """
    階段を一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    sequence_table: np.array((5,15))
        持っているカードで構成出来る階段の情報を示す配列 ref:  tableMaker
    scope: list(int)
        構成する組を置くための探索順序を示すリスト
        昇順なら弱いカード, 降順なら強いカードを選択する

    Return
    ------
    one_seq_table: np.array((5,15))
        選んだ一つの階段を示す配列
    """
    one_seq_table = np.zeros_like(cards, dtype=int)

    for rank in scope:
        for suit in range(4):
            if sequence_table[suit, rank] > 0:
                for con_num in range(sequence_table[suit, rank]):
                    if cards[suit, rank + con_num] == 1:
                        one_seq_table[suit, rank + con_num] = 1
                    else:  # なければjokerを使う(Sequenceなので足りないならJOKERを使っていると判定して大丈夫)
                        one_seq_table[suit, rank + con_num] = 2
                return one_seq_table
    return one_seq_table

# Helper --


def selectLowSequence(cards, sequence_table, joker_flag=False):
    """
    階段を弱い方から一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    sequence_table: np.array((5,15))
        持っているカードで構成出来る階段の情報を示す配列 ref:  tableMaker
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一つの階段を示す配列
    """
    return selectBaseSequence(cards, sequence_table, range(15))


def selectHighSequence(cards, sequence_table, joker_flag=False):
    """
    階段を強い方から一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    sequence_table: np.array((5,15))
        持っているカードで構成出来る階段の情報を示す配列 ref:  tableMaker
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一つの階段を示す配列
    """
    return selectBaseSequence(cards, sequence_table, reversed(range(15)))

# Pair ---
# Base --


def selectBasePair(cards, pair_table, subsutitute, scope, bind_suit):
    """
    ペアを一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    pair_table: np.array((5,15))
        持っているカードで構成出来る組の情報を示す配列 ref:  tableMaker
    substitute: int
        組を構成するカードが足りない場合に使う数値
        JOKERを使うのであれば2, 使わないのであれば0
    scope: list(int)
        構成する組を置くための探索順序を示すリスト
        昇順なら弱いカード, 降順なら強いカードを選択する
    bind_suit: list(int)
        カードを置ける範囲を指定する

    Return
    ------
    one_pair_table: np.array((5,15))
        選んだ一つの組を示す配列
    """
    one_pair_table = np.zeros_like(cards, dtype=int)

    for rank in scope:
        for suit in range(4):
            if pair_table[suit, rank] > 0:
                quantity = pair_table[suit, rank]
                set_sub = (sum(cards[:, rank]) == quantity)
                set_cnt = 0
                for con_suit in range(5):
                    if set_cnt == quantity:
                        break
                    if con_suit not in bind_suit:
                        continue

                    if cards[con_suit, rank] == 1:
                        one_pair_table[con_suit, rank] = 1
                        set_cnt += 1
                    elif not set_sub:
                        one_pair_table[con_suit, rank] = subsutitute
                        set_cnt += 1 if subsutitute == 2 else 0
                        set_sub = True
                return one_pair_table
    return one_pair_table

# Helper --


def selectLowPair(cards, pair_table, bind_suit=range(5), joker_flag=False):
    """
    ペアを弱い方から一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    pair_table: np.array((5,15))
        持っているカードで構成出来る組の情報を示す配列 ref:  tableMaker
    bind_suit: list(int)
        提出可能な絵柄を示すリスト
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一つの組を示す配列
    """
    return selectBasePair(cards, pair_table, 2 if joker_flag else 0, range(15), bind_suit=bind_suit)


def selectHighPair(cards, pair_table, bind_suit=range(5), joker_flag=False):
    """
    ペアを強い方から一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    pair_table: np.array((5,15))
        持っているカードで構成出来る組の情報を示す配列 ref:  tableMaker
    bind_suit: list(int)
        提出可能な絵柄を示すリスト
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一つの組を示す配列
    """
    return selectBasePair(cards, pair_table, 2 if joker_flag else 0, reversed(range(15)), bind_suit=bind_suit)

# Single ---


def selectBaseSingle(cards, subsutitute, scope):
    """
    単騎を一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    substitute: int
        通常のカードがない場合に使う数値
        JOKERを使うのであれば2, 使わないのであれば0
    scope: list(int)
        構成する組を置くための探索順序を示すリスト
        昇順なら弱いカード, 降順なら強いカードを選択する

    Return
    ------
    single_table: np.array((5,15))
        選んだ一枚を示す配列
    """
    single_table = np.zeros_like(cards, dtype=int)

    for rank in scope:
        for suit in range(4):
            if cards[suit, rank] > 0:
                single_table[suit, rank] = 1
                return single_table

    # まだreturnされていないならJOKERか0を入れて返す
    single_table[0, 14] = subsutitute
    return single_table


def selectLowSingle(cards, joker_flag=False):
    """
    弱い方から単騎を一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一枚を示す配列
    """
    return selectBaseSingle(cards, 2 if joker_flag else 0, range(15))


def selectHighSingle(cards, joker_flag=False):
    """
    強い方から単騎を一つ選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    joker_flag: bool
        JOKERを使うかどうかのフラグ

    Return
    ------
    np.array((5,15))
        選んだ一枚を示す配列
    """
    return selectBaseSingle(cards, 2 if joker_flag else 0, reversed(range(15)))
