import numpy as np

# フィルタに関する関数群


def applyFilter(cards, field_info, info):
    """
    フィルタ適応により提出不能なカードを手札から除外する
    非革命時にのみ適応可

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    field_info: dict
        場のカードの情報 ref:  parser
    info: dict
        サーバから送られてくる情報 ref:  parser

    Return
    ------
    filtered_cards: np.array((5,15))
        現在の場に対して提出可能になりうるカードを示す配列
    """
    filtered_cards = excludeLow(cards, max(field_info['rank']))
    if info['binded']:
        filtered_cards = excludeNotInSuit(filtered_cards, field_info['suit'])
    return filtered_cards


def applyRevFilter(cards, field_info, info):
    """
    フィルタ適応により提出不能なカードを手札から除外する
    革命時にのみ適応可

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    field_info: dict
        場のカードの情報 ref:  parser
    info: dict
        サーバから送られてくる情報 ref:  parser

    Return
    ------
    filtered_cards: np.array((5,15))
        現在の場に対して提出可能になりうるカードを示す配列
    """
    filtered_cards = excludeHigh(cards, min(field_info['rank']))
    if info['binded']:
        filtered_cards = excludeNotInSuit(filtered_cards, field_info['suit'])
    return filtered_cards

# Filters -----
# By rank ---


def excludeLow(cards, rank):
    """
    強さがrank以下のカードをcardsから除外する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    rank: int
        除外する強さの基準値

    Return
    ------
    filtered_cards: np.array((5,15))
        フィルタを適用した後の配列
    """
    filtered_cards = np.array(cards, dtype=int)
    filtered_cards[:, :rank+1] = 0
    return filtered_cards


def excludeHigh(cards, rank):
    """
    強さがrank以上のカードをcardsから除外する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    rank: int
        除外する強さの基準値

    Return
    ------
    filtered_cards: np.array((5,15))
        フィルタを適用した後の配列
    """
    filtered_cards = np.array(cards, dtype=int)
    filtered_cards[:, rank:] = 0
    return filtered_cards

# By suit ---


def excludeNotInSuit(cards, suit):
    """
    絵柄がsuitに含まれないカードをcardsから取り除く

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    suit: list(int)
        除外しない絵柄を示すリスト

    Return
    ------
    filtered_cards: np.array((5,15))
        フィルタを適用した後の配列
    """
    filtered_cards = np.zeros_like(cards, dtype=int)
    filtered_cards[suit, :] = cards[suit, :]
    return filtered_cards

# By value ---


def excludeNotN(table, n):
    """
    値がnでない要素をcardsから取り除く

    Parameters
    ----------
    table: np.array((5,15))
        組や階段の構成を示す配列
    n: int
        除外しない基準値

    Return
    ------
    filtered_table: np.array((5,15))
        フィルタを適用した後の配列
    """
    return (table == n) * n
