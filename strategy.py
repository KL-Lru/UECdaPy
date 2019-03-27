import numpy as np
from utils import *


def selectExchangeCards(cards, info):
    """
    手札交換で提出するカードを選択する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser
    """

    # 弱い方から必要枚数選択
    quantity = info['exchange_quantity']
    work_table = np.zeros_like(cards)
    while quantity > 0:
        work_table += selectLowSingle(cardDiff(cards, work_table))
        quantity -= 1

    return work_table


def selectFlushCards(cards, info):
    """
    場札のない時に提出するカードを選択する
    非革命時を想定する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser
    """
    sequence_table, pair_table = makeTables(cards, info)

    # 階段優先で選択
    if existConstitution(sequence_table):
        for quantity in reversed(range(3, 15)):
            n_table = excludeNotN(sequence_table, quantity)
            if existConstitution(n_table):
                return selectLowSequence(cards, n_table, info['have_joker'])

    # なければ組で選択
    if existConstitution(pair_table):
        for quantity in reversed(range(2, 6)):
            n_table = excludeNotN(pair_table, quantity)
            if existConstitution(n_table):
                return selectLowPair(cards, n_table, joker_flag=info['have_joker'])

    # なければ単騎で選択
    return selectLowSingle(cards, info['have_joker'])


def selectFlushRevCards(cards, info):
    """
    場札のない時に提出するカードを選択する
    革命時を想定する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser
    """
    sequence_table, pair_table = makeTables(cards, info)

    # 階段優先で選択
    if existConstitution(sequence_table):
        for quantity in reversed(range(3, 15)):
            n_table = excludeNotN(sequence_table, quantity)
            if existConstitution(n_table):
                return selectHighSequence(cards, n_table, info['have_joker'])

    # なければ組で選択
    if existConstitution(pair_table):
        for quantity in reversed(range(2, 6)):
            n_table = excludeNotN(pair_table, quantity)
            if existConstitution(n_table):
                return selectHighPair(cards, n_table, joker_flag=info['have_joker'])

    # なければ単騎で選択
    return selectHighSingle(cards, info['have_joker'])


def selectFollowCards(cards, field, info):
    """
    場札のある時に提出するカードを選択する
    非革命時を想定する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    field: np.array((5,15))
        場札を示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser
    """
    field_info = parseFieldCards(field)
    filtered_cards = applyFilter(cards, field_info, info)
    sequence_table, pair_table = makeTables(filtered_cards, info)

    # 階段ではJOKERを使う際に強さが場にあるカードと被る階段を構成するのを防ぐ
    sequence_table[:, max(field_info['rank'])] = 0

    if field_info['type'] == 'sequence':
        n_table = excludeNotN(sequence_table, field_info['quantity'])
        if existConstitution(n_table):
            return selectLowSequence(filtered_cards, n_table, info['have_joker'])
        return np.zeros_like(cards)

    if field_info['type'] == 'pair':
        n_table = excludeNotN(pair_table, field_info['quantity'])
        if existConstitution(n_table):
            if info['binded']:
                return selectLowPair(filtered_cards, n_table, field_info['suit'], info['have_joker'])
            else:
                return selectLowPair(filtered_cards, n_table, joker_flag=info['have_joker'])
        return np.zeros_like(cards)

    # まだ提出されていないのなら場札は単騎
    # ペアになっているカードや階段を構成できるカードは除外しておく
    filtered_cards = cardDiff(filtered_cards, expandSequence(sequence_table))
    filtered_cards = cardDiff(filtered_cards, expandPair(pair_table))

    return selectLowSingle(filtered_cards, joker_flag=info['have_joker'])


def selectFollowRevCards(cards, field, info):
    """
    場札のある時に提出するカードを選択する
    革命時を想定する

    Parameters
    ----------
    cards: np.array((5,15))
        持っているカードを示す配列
    field: np.array((5,15))
        場札を示す配列
    info: dict
        サーバから送られてくる情報 ref:  parser
    """
    field_info = parseFieldCards(field)
    filtered_cards = applyRevFilter(cards, field_info, info)
    sequence_table, pair_table = makeTables(filtered_cards, info)

    # 階段ではJOKERを使う際に強さが場にあるカードと被る階段を構成するのを防ぐ
    sequence_table[:, min(field_info['rank'])] = 0

    if field_info['type'] == 'sequence':
        n_table = excludeNotN(sequence_table, field_info['quantity'])
        if existConstitution(n_table):
            return selectHighSequence(filtered_cards, n_table, info['have_joker'])
        return np.zeros_like(cards)

    if field_info['type'] == 'pair':
        n_table = excludeNotN(pair_table, field_info['quantity'])
        if existConstitution(n_table):
            if info['binded']:
                return selectHighPair(filtered_cards, n_table, field_info['suit'], info['have_joker'])
            else:
                return selectHighPair(filtered_cards, n_table, joker_flag=info['have_joker'])
        return np.zeros_like(cards)

    # まだ提出されていないのなら場札は単騎
    # ペアになっているカードや階段を構成できるカードは除外しておく
    filtered_cards = cardDiff(filtered_cards, expandSequence(sequence_table))
    filtered_cards = cardDiff(filtered_cards, expandPair(pair_table))
    return selectHighSingle(filtered_cards, joker_flag=info['have_joker'])
